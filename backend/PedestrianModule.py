import os
import json
from tqdm import tqdm

import cv2
import numpy as np

from RuleProcessor import RuleProcessor
from ObjectDetectionModule import ObjectDetectionModule


class PedestrianModule(RuleProcessor):
    '''
    This class detects if vehicles do not stop for pedestrians to cross
    '''

    def __init__(self, videoData):
        super().__init__(videoData)
        self.num_violations = 0
        self.frame_saved = -100
        self.current_frame_num = -1
        self.waiting_boxes = []
        self.crossing_boxes = []

    def set_metadata(self, metadata):
        waiting_box = metadata['pedestrian_area']
        crossing_box = metadata['zebra_crossing']
        refactored_waiting_box = self.refactor_box(waiting_box)
        refactored_crossing_box = self.refactor_box(crossing_box)

        self.waiting_boxes.append(refactored_waiting_box)
        self.crossing_boxes.append(refactored_crossing_box)

    def refactor_box(self, box):
        min_x = 5000
        min_y = 5000
        max_x = -2
        max_y = -2

        for c in box:
            if int(c[0]) < min_x:
                min_x = c[0]
            if int(c[0]) > max_x:
                max_x = c[0]
            if int(c[1]) < min_y:
                min_y = c[1]
            if int(c[1]) > max_y:
                max_y = c[1]

        refactored_box = [min_x, min_y, max_x, max_y]

        return refactored_box

    def process_rule(self):
        self.output_video_data = []

        self.objectD = ObjectDetectionModule(self.input_video_data)

        for composite_frame in self.input_video_data:
            self.current_frame_num += 1
            current_frame = composite_frame

            detected_object_boxes, box_labels, _ = self.objectD.detect_objects_in_frame(
                current_frame)

            output_frame = self.draw_pedestrian_boxes(current_frame)

            output_frame = self.detect_violation(
                current_frame, detected_object_boxes, box_labels)

            self.output_video_data.append(output_frame)

    def draw_pedestrian_boxes(self, frame):
        for box_type in [self.waiting_boxes, self.crossing_boxes]:
            for box in box_type:
                box = [int(u) for u in box]
                top_left_corner = tuple(box[:2])
                bottom_right_corner = tuple(box[2:])

                cv2.putText(frame, "Pedestrian Area", (
                    top_left_corner[0], top_left_corner[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
                cv2.rectangle(frame, top_left_corner,
                              bottom_right_corner, (255, 0, 0), 2)

        return frame

    def detect_violation(self, frame, object_boxes, labels):
        num_pedestrian_areas = len(self.crossing_boxes)

        pedestrian_waiting = False
        vehicle_crossing = False

        violating_objects = []

        vehicle_list = ['motorbike', 'bus', 'truck', 'car']

        for i in range(num_pedestrian_areas):
            for obj, label in zip(object_boxes, labels):
                if self.objectD.class_names[label] == 'person':
                    if self.object_in_box(obj, self.waiting_boxes[i]) or self.object_in_box(obj, self.crossing_boxes[i]):
                        violating_objects.append(obj)
                        pedestrian_waiting = True

                elif self.objectD.class_names[label] in vehicle_list:
                    if self.object_in_box(obj, self.crossing_boxes[i]):
                        violating_objects.append(obj)
                        vehicle_crossing = True

            if pedestrian_waiting == True and vehicle_crossing == True:
                frame = self.draw_violating_objects(frame, violating_objects)
                self.add_snapshot(frame)

        return frame

    def object_in_box(self, obj, box):
        left = right = [0, 0, 0, 0]
        top = bottom = [0, 0, 0, 0]
        if obj[0] <= box[0]:
            left = obj
            right = box
        else:
            left = box
            rigth = obj

        if obj[1] <= box[1]:
            top = obj
            bottom = box
        else:
            top = box
            bottom = obj

        if left[2] < right[0] or top[3] < bottom[1]:
            return False
        else:
            return True

    def draw_violating_objects(self, frame, violating_objects):
        for obj in violating_objects:
            top_left_corner = (obj[0], obj[1])
            top_left_corner = tuple(obj[:2])
            bottom_right_corner = tuple(obj[2:])
            cv2.rectangle(frame, top_left_corner,
                          bottom_right_corner, (0, 0, 255), 2)

        return frame

    def add_snapshot(self, frame):
        if self.current_frame_num - self.frame_saved >= 25:
            self.num_violations += 1
            self.snapshot_data.append([frame, self.num_violations])
            self.frame_saved = self.current_frame_num

    def output_snapshots(self):
        for snap in self.snapshot_data:
            snapshot_name = 'pedestrian_violation_' + \
                str(snap[1]) + '.jpg'
            cv2.imwrite('pedestrian/images/' + snapshot_name, snap[0])


if __name__ == '__main__':
    vc = cv2.VideoCapture('pedestrian.mp4')

    frame_number = 0
    frame_list = []

    n_frames = int(cv2.CAP_PROP_FRAME_COUNT)
    frame_rate = int(vc.get(cv2.CAP_PROP_FPS))
    number_of_frames = vc.get(n_frames)
    print(number_of_frames, frame_rate)
    while frame_number < number_of_frames:
        frame_number += 1
        (frame_grabbed, current_frame) = vc.read()
        if not frame_grabbed:
            break

        frame_list.append(current_frame)

    print(len(frame_list))

    objectP = PedestrianModule(frame_list)
    objectP.set_frame_rate(frame_rate)
    objectP.set_metadata({'zebra_crossing': [
                         150, 780, 1600, 950], 'pedestrian_area': [1600, 770, 1800, 950]})
    objectP.process_rule()

    objectP.output_snapshots()
    frames = objectP.output_processed_frames()

    W = frames[0].shape[1]
    H = frames[0].shape[0]
    out = cv2.VideoWriter(
        'pedestrian/video/project.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (W, H))

    for frame in frames:
        out.write(frame)
    out.release()
