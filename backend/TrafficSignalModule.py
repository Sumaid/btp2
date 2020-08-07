import os
import json
from tqdm import tqdm

import cv2
import numpy as np

from RuleProcessor import RuleProcessor
from ObjectDetectionModule import ObjectDetectionModule


class TrafficSignalModule(RuleProcessor):
    '''
    This class detects if vehicles violate traffic signal rules
    '''

    def __init__(self, videoData):
        super().__init__(videoData)
        self.num_violations = 0
        self.frame_saved = -100
        self.current_frame_num = -1
        self.traffic_box = []
        self.traffic_signal = []

    def set_metadata(self, metadata):
        box = metadata['zebra_crossing']
        self.traffic_box = self.refactor_box(box)

    def refactor_box(self, box):
        min_x = 5000
        min_y = 5000
        max_x = -2
        max_y = -2

        for c in box:
            if c[0] < min_x:
                min_x = c[0]
            if c[0] > max_x:
                max_x = c[0]
            if c[1] < min_y:
                min_y = c[1]
            if c[1] > max_y:
                max_y = c[1]

        refactored_box = [min_x, min_y, max_x, max_y]
        return refactored_box

    def process_rule(self):
        self.output_video_data = []

        self.objectD = ObjectDetectionModule(self.input_video_data)

        self.traffic_signal = self.simulate_signal()

        for composite_frame in self.input_video_data:
            self.current_frame_num += 1
            current_frame = composite_frame

            detected_object_boxes, box_labels, _ = self.objectD.detect_objects_in_frame(
                current_frame)

            output_frame = self.draw_traffic_box(current_frame)

            output_frame = self.detect_violation(
                current_frame, detected_object_boxes, box_labels)

            self.output_video_data.append(output_frame)

    def simulate_signal(self):
        signal = []
        for i in range(305):
            signal.append(0)
        for i in range(94):
            signal.append(1)
        return signal

    def draw_traffic_box(self, frame):
        top_left_corner = tuple(self.traffic_box[:2])
        bottom_right_corner = tuple(self.traffic_box[2:])

        cv2.rectangle(frame, top_left_corner,
                      bottom_right_corner, (0, 255, 0), 2)

        return frame

    def detect_violation(self, frame, object_boxes, labels):
        vehicle_crossing = False

        violating_objects = []

        vehicle_list = ['motorbike', 'bus', 'truck', 'car', 'bicycle']

        if self.traffic_signal[self.current_frame_num] == 0:
            for obj, label in zip(object_boxes, labels):
                if self.objectD.class_names[label] in vehicle_list:
                    if self.object_in_box(obj, self.traffic_box):
                        violating_objects.append(obj)
                        vehicle_crossing = True

            if vehicle_crossing == True:
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
            snapshot_name = 'trafficsignal_violation_' + \
                str(snap[1]) + '.jpg'
            cv2.imwrite('trafficsignal/images/' + snapshot_name, snap[0])


if __name__ == '__main__':
    vc = cv2.VideoCapture('trafficsignal.mp4')

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

    objectT = TrafficSignalModule(frame_list)
    objectT.set_frame_rate(frame_rate)
    objectT.set_metadata({'zebra_crossing': [800, 450, 1300, 470]})
    objectT.process_rule()

    objectT.output_snapshots()
    frames = objectT.output_processed_frames()

    W = frames[0].shape[1]
    H = frames[0].shape[0]
    out = cv2.VideoWriter(
        'trafficsignal/video/project.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (W, H))

    for frame in frames:
        out.write(frame)
    out.release()
