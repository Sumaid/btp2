import os
import sys
import json
from tqdm import tqdm

import cv2
import numpy as np

from RuleProcessor import RuleProcessor
from ObjectDetectionModule import ObjectDetectionModule


class CrashDetectionModule(RuleProcessor):
    '''
    This class detects if there is a crash in a video
    '''

    def __init__(self, videoData):
        super().__init__(videoData)
        self.total_crashes = 0
        self.frame_saved = -100
        self.current_frame_num = -1
        self.objects_to_monitor = [0, 2, 5, 7]
        self.collision_relaxation_x = 0.9
        self.collision_relaxation_y = 0.5

    def process_rule(self):
        self.output_video_data = []
        self.objectD = ObjectDetectionModule(self.input_video_data)

        for composite_frame in self.input_video_data:
            self.current_frame_num += 1
            current_frame = composite_frame

            detected_object_boxes, box_labels, _ = self.objectD.detect_objects_in_frame(
                current_frame)

            output_frame = self.detect_crash(
                current_frame, detected_object_boxes, box_labels)

            self.output_video_data.append(output_frame)

    def detect_crash(self, current_frame, boxes, box_labels):

        if len(boxes) > 0:
            crashObjects = self.get_crash_objects_list(box_labels)

            flag = 0
            for j in crashObjects:
                for k in crashObjects:
                    if k == j:  # same objects
                        continue

                    crashing_objects = []
                    object1_crash_variables = self.get_overlap_variables(
                        boxes[j])
                    object2_crash_variables = self.get_overlap_variables(
                        boxes[k])

                    if self.detect_overlap(object1_crash_variables, object2_crash_variables):
                        crashing_objects.append(boxes[j])
                        crashing_objects.append(boxes[k])
                        current_frame = self.draw_crashing_objects(
                            current_frame, crashing_objects)
                        self.add_snapshot(current_frame)

        return current_frame

    def get_crash_objects_list(self, box_labels):
        crashObjects = []
        for j in range(len(box_labels)):
            if box_labels[j] in self.objects_to_monitor:
                crashObjects.append(j)

        return crashObjects

    def get_overlap_variables(self, box):
        (lx, ly) = (box[0], box[1])
        (rx, ry) = (box[2], box[3])
        (w, h) = (abs(rx-lx), abs(ly-ry))
        (cx, cy) = ((lx+rx)/2, (ly+ry)/2)

        return [w, h, cx, cy]

    def detect_overlap(self, object1_crash_variables, object2_crash_variables):
        distance_between_centers_x = abs(
            object1_crash_variables[2] - object2_crash_variables[2])
        distance_allowed_x = (
            object1_crash_variables[0]/2 + object2_crash_variables[0]/2) * (self.collision_relaxation_x)

        distance_between_centers_y = abs(
            object1_crash_variables[3] - object2_crash_variables[3])
        distance_allowed_y = (
            object1_crash_variables[1]/2 + object2_crash_variables[1]/2) * (self.collision_relaxation_y)

        if (distance_between_centers_x < distance_allowed_x and distance_between_centers_y < distance_allowed_y):
            return True

    def draw_crashing_objects(self, frame, crashing_objects):
        for obj in crashing_objects:
            top_left_corner = tuple(obj[:2])
            bottom_right_corner = tuple(obj[2:])
            cv2.rectangle(frame, top_left_corner,
                          bottom_right_corner, (0, 0, 255), 2)
        return frame

    def add_snapshot(self, frame):
        if self.current_frame_num - self.frame_saved >= self.frame_rate:
            self.total_crashes += 1
            self.snapshot_data.append([frame, self.total_crashes])
            self.frame_saved = self.current_frame_num

    def output_snapshots(self):
        for snap in self.snapshot_data:
            snapshot_name = 'crash_detection_' + str(snap[1]) + '.jpg'
            cv2.imwrite('crash/images/' + snapshot_name, snap[0])


# class objectDetectionModule(RuleProcessor):
#     '''
#     The class for the basic object detection module, which can be used for
#     display in the frontend
#     '''

#     def __init__(self, videoData):
#         super().__init__(videoData)
#         self.initialize_yolo_settings('settings.json')
#         self.initialize_net()

#     def initialize_yolo_settings(self, YOLO_PATH):
#         settings = self.read_settings_from_json(YOLO_PATH)

#         config_full_path = [settings['YOLO_PATH'],
#                             settings["YOLO_CONFIG_FILE"]]
#         weights_full_path = [settings['YOLO_PATH'],
#                              settings["YOLO_WEIGHTS_FILE"]]
#         class_names_full_path = [settings['YOLO_PATH'], settings["NAMES_FILE"]]

#         self.net_config_path = os.path.sep.join(config_full_path)
#         self.net_weights_path = os.path.sep.join(weights_full_path)
#         self.class_names_path = os.path.sep.join(class_names_full_path)

#         self.confidence_threshold = 0.5  # Confidence threshold
#         self.nms_threshold = 0.4  # Non-maximum suppression threshold
#         self.net_input_dims = (416, 416)  # Size of network's input image
#         self.frame_dimensions = None

#         with open(self.class_names_path) as fp:
#             self.class_names = [u.strip() for u in fp.readlines()]

#     def initialize_net(self):
#         self.net = cv2.dnn.readNetFromDarknet(
#             self.net_config_path, self.net_weights_path)
#         self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
#         self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

#         layer_names_temp = self.net.getLayerNames()
#         self.layer_names = [layer_names_temp[i[0] - 1]
#                             for i in self.net.getUnconnectedOutLayers()]

#     def read_settings_from_json(self, path):
#         with open(path) as f:
#             settings_data = json.load(f)
#         return settings_data

#     def process_rule(self):
#         self.output_video_data = []

#         for composite_frame in self.input_video_data:
#             current_frame = composite_frame

#             detected_object_boxes, box_labels = self.detect_objects_in_frame(
#                 current_frame)
#             output_frame = self.draw_boxes_on_frame(
#                 current_frame, detected_object_boxes, box_labels)

#             self.output_video_data.append(output_frame)

#     def detect_objects_in_frame(self, frame):
#         if self.frame_dimensions == None:
#             self.frame_dimensions = frame.shape[:2][::-1]

#         blob_ = cv2.dnn.blobFromImage(
#             frame, 1 / 255, self.net_input_dims, swapRB=True)
#         net_outputs = self.forward_through_net(blob_)
#         bounding_boxes, class_labels = self.get_bounding_boxes(
#             net_outputs)
#         return bounding_boxes, class_labels

#     def forward_through_net(self, blob):
#         self.net.setInput(blob)
#         layer_outputs = self.net.forward(self.layer_names)
#         return layer_outputs

#     def get_bounding_boxes(self, net_outputs):
#         bounding_box_list, confidence_list, class_labels = self.extract_naive_boxes(
#             net_outputs)
#         boxes_metadata = {
#             'confidences': confidence_list, 'labels': class_labels}
#         nms_refactored_boxes, final_class_labels = self.extract_refactored_boxes(
#             bounding_box_list, boxes_metadata)
#         return nms_refactored_boxes, final_class_labels

#     def extract_naive_boxes(self, output_list):
#         boxes = []
#         class_labels = []

#         confidences = []

#         for output in output_list:
#             for detection in output:
#                 confidence_scores = detection[5:]
#                 predicted_class = np.argmax(confidence_scores)

#                 predicted_class_confd = confidence_scores[predicted_class]

#                 if predicted_class_confd > self.confidence_threshold:
#                     original_width, original_height = self.frame_dimensions
#                     rescaling_factor = [
#                         original_width, original_height, original_width, original_height]

#                     box = np.array(detection[:4] * np.array(rescaling_factor))

#                     box_centre_x, box_centre_y, box_width, box_height = box.astype(
#                         "int")
#                     top_left_corner_x = int(box_centre_x - 0.5 * box_width)
#                     top_left_corner_y = int(box_centre_y - 0.5 * box_height)

#                     box = [top_left_corner_x, top_left_corner_y,
#                            box_width, box_height]
#                     boxes.append(box)
#                     class_labels.append(predicted_class)
#                     confidences.append(predicted_class_confd)

#         return boxes, confidences, class_labels

#     def extract_refactored_boxes(self, boxes, boxes_metadata):
#         boxes = [np.array(box).astype(int) for box in boxes]
#         confidences = [float(confidence)
#                        for confidence in boxes_metadata['confidences']]

#         index_list = cv2.dnn.NMSBoxes(
#             boxes, confidences, self.confidence_threshold, self.nms_threshold)

#         final_boxes = []
#         final_class_labels = []

#         if len(index_list):
#             for i in index_list.flatten():
#                 box_width, box_height = boxes[i][2], boxes[i][3]

#                 top_left_corner = boxes[i][0], boxes[i][1]
#                 bottom_right_corner = (
#                     top_left_corner[0] + box_width, top_left_corner[1] + box_height)

#                 box_details = [*top_left_corner, *bottom_right_corner]
#                 final_boxes.append(box_details)
#                 final_class_labels.append(boxes_metadata['labels'][i])

#         return final_boxes, final_class_labels

#     def draw_boxes_on_frame(self, frame, boxes, labels):
#         for box, label in zip(boxes, labels):
#             top_left_corner = tuple(box[:2])
#             bottom_right_corner = tuple(box[2:])

#             cv2.putText(frame, self.class_names[label], (top_left_corner[0]-50,
#                                                          top_left_corner[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
#             cv2.rectangle(frame, top_left_corner,
#                           bottom_right_corner, (0, 0, 255), 2)

#         return frame

#     def output_processed_frames(self):
#         return self.output_video_data


if __name__ == '__main__':
    vc = cv2.VideoCapture('crashdetection.mp4')

    frame_number = 0
    frame_list = []

    n_frames = int(cv2.CAP_PROP_FRAME_COUNT)
    frame_rate = int(vc.get(cv2.CAP_PROP_FPS))
    number_of_frames = vc.get(n_frames)
    print(number_of_frames)
    while frame_number < number_of_frames:
        frame_number += 1
        (frame_grabbed, current_frame) = vc.read()
        if not frame_grabbed:
            break

        frame_list.append(current_frame)

    assert(len(frame_list) == number_of_frames)

    objectC = CrashDetectionModule(frame_list)
    objectC.process_rule()
    print("Crashes detected")
