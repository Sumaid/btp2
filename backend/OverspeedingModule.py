import sys
from RuleProcessor import RuleProcessor

from ObjectDetectionModule import ObjectDetectionModule

from sort import *
import numpy as np

import matplotlib.pyplot as plt

import cv2
import time
from tqdm import tqdm

import secrets
import warnings
warnings.filterwarnings("ignore")


def check_line_intersection(line_0, line_1):
    
    def ccw_check(point_0, point_1, point_2):
        lhs = (point_2[1] - point_0[1]) * (point_1[0] - point_0[0])
        rhs = (point_1[1] - point_0[1]) * (point_2[0] - point_0[0])
        
        return lhs > rhs
    
    line_0_start, line_0_end = line_0
    line_1_start, line_1_end = line_1
    
    ccw_check_1 = ccw_check(line_0_start, line_1_start, line_1_end)
    ccw_check_2 = ccw_check(line_0_end, line_1_start, line_1_end)
    ccw_check_3 = ccw_check(line_0_start, line_0_end, line_1_start)
    ccw_check_4 = ccw_check(line_0_start, line_0_end, line_1_end)

    return ccw_check_1 != ccw_check_2 and ccw_check_3 != ccw_check_4

class OverspeedingModule(RuleProcessor):
    def __init__(self, videoData):
        super().__init__(videoData)
        self.tracker = Sort()
        self.frame_dimensions = None
        self.lane_ = None
        
        self.objectDetector = ObjectDetectionModule()
        
    def set_metadata(self, metadata):
        line = metadata['lane_data']
        self.speed_start_line = tuple([tuple(line[0]), tuple(line[1])])
        self.speed_end_line = tuple([tuple(line[2]), tuple(line[3])])
        self.road_distance = int(metadata['road_length'])
        self.speed_limit = int(metadata['speed_limit'])
        
        self.snapshot_path = 'overspeed/images/'
        self.time_tracker = {}

    def process_rule(self):
        self.output_video_data = []
        
        memory = {}
        current_frame_number = 0
        
        for current_frame in tqdm(self.input_video_data):
            if self.frame_dimensions == None:
                self.frame_dimensions = current_frame.shape[:2][::-1]
            
            detected_object_boxes, labels, confidences = self.objectDetector.detect_objects_in_frame(current_frame)
            detected_object_boxes = np.array(detected_object_boxes)
            confidences_np_array = np.array([confidences]).T
            try:
                tracker_input = np.append(detected_object_boxes, confidences_np_array, axis=1)
                time_tracked_objects = self.tracker.update(tracker_input)
                
                box_list = []
                box_indexID = []
                
                previous_memory = memory.copy()
                memory = {}

                i = 0
                
                for track in time_tracked_objects:
                    box_list.append([track[0], track[1], track[2], track[3]])
                    box_indexID.append(int(track[4]))
                    memory[box_indexID[-1]] = box_list[-1]
        
                for box in box_list:
                    box = [int(box_detail) for box_detail in box]
                    box_center = self.get_center_of_box(box)
                    
                    current_id = box_indexID[i]
                    
                    if current_id in previous_memory:
                        previous_box = previous_memory[current_id]
                        
                        box_previous_center = self.get_center_of_box(previous_box)
                        car_track_line = (box_center, box_previous_center)

                        if check_line_intersection(car_track_line, self.speed_start_line):
                            measure_time_start = current_frame_number
                            self.time_tracker.update({current_id: measure_time_start})
                            
                        elif check_line_intersection(car_track_line, self.speed_end_line):
                            try:
                                frames_taken = current_frame_number - self.time_tracker.get(current_id)
                                speed = self.calculate_speed(frames_taken)
                                if speed > self.speed_limit:
                                    print("Yes")
                                    self.add_snapshot(current_frame, box, speed, current_frame_number)
                                del self.time_tracker[current_id]
                            except:
                                pass
                    i += 1
                current_frame_number += 1
                self.output_video_data.append(current_frame)
            except:
                pass
    
    def get_center_of_box(self, box):
        box_center_x = np.mean((box[0], box[2]))
        box_center_y = np.mean((box[1], box[3]))
        box_center = (box_center_x, box_center_y)
        return box_center
    
    def calculate_speed(self, frames_taken):
        time_taken = frames_taken / self.frame_rate
        speed = int(3.6 * self.road_distance / time_taken)
        return speed
    
    def add_snapshot(self, current_frame, box, speed, current_frame_number):
        a,b = tuple(box[:2]), tuple(box[2:])
        cv2.rectangle(current_frame, a, b, (0, 0, 255), 1)
        video_seektime = current_frame_number * self.frame_rate
        
        self.snapshot_data.append([current_frame, speed, video_seektime])
    
    def output_snapshots(self):
        for snap in self.snapshot_data:
            snapshot_name = str(snap[1]) + '_' + str(snap[2]) + 's_' + secrets.token_hex(7) + '.jpg'

            cv2.imwrite(self.snapshot_path+snapshot_name, snap[0])

if __name__ == '__main__':
    vc = cv2.VideoCapture('overspeeding.mp4')
    
    frame_number = 0
    frame_list = []
    
    n_frames = int(cv2.CAP_PROP_FRAME_COUNT)
    number_of_frames = vc.get(n_frames)
    
    print(number_of_frames)
    while frame_number < number_of_frames:
        frame_number += 1
        (frame_grabbed, current_frame) = vc.read()
        if not frame_grabbed:
            break

        frame_list.append(current_frame)

    print(len(frame_list))
    m = {
        'speed_limit': 10, 
        'lane_data' :[[7,209],[605,208],[604,187],[7,187]],
        'road_length': 100
    }
    objectD = OverspeedingModule(frame_list)
    objectD.set_metadata(m)
    objectD.set_frame_rate(25)
    
    objectD.process_rule()

    frames = objectD.output_processed_frames() # Return a list of output frames
    
    objectD.output_snapshots()
    exit()
    out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 25, (640,360))

    for frame in frames:
        out.write(frame)
    out.release()
