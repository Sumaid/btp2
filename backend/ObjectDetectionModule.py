import os
import json
from tqdm import tqdm

import cv2
import numpy as np

from RuleProcessor import RuleProcessor

class ObjectDetectionModule(RuleProcessor):
    '''
    The class for the basic object detection module, which can be used for 
    display in the frontend 
    '''
    def __init__(self, videoData = None):
        super().__init__(videoData)
        
        self.initialize_yolo_settings('settings.json')
        self.initialize_net()
    
    def initialize_yolo_settings(self, YOLO_PATH):
        settings = self.read_settings_from_json(YOLO_PATH)
        
        config_full_path = [settings['YOLO_PATH'], settings["YOLO_CONFIG_FILE"]]
        weights_full_path = [settings['YOLO_PATH'], settings["YOLO_WEIGHTS_FILE"]]
        class_names_full_path = [settings['YOLO_PATH'], settings["NAMES_FILE"]]
        
        self.net_config_path = os.path.sep.join(config_full_path)
        self.net_weights_path = os.path.sep.join(weights_full_path)
        self.class_names_path = os.path.sep.join(class_names_full_path)
        
        self.confidence_threshold = 0.5       #Confidence threshold
        self.nms_threshold = 0.4              #Non-maximum suppression threshold
        self.net_input_dims = (416, 416)      #Size of network's input image
        
        with open(self.class_names_path) as fp:
            self.class_names = [u.strip() for u in fp.readlines()]
    
    def initialize_net(self):
        self.net = cv2.dnn.readNetFromDarknet(self.net_config_path, self.net_weights_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        
        layer_names_temp = self.net.getLayerNames()
        self.layer_names = [layer_names_temp[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        
    def read_settings_from_json(self, path):
        with open(path) as f:
            settings_data = json.load(f)
        return settings_data

    def process_rule(self):
        self.output_video_data = []
        
        for composite_frame in tqdm(self.input_video_data):
            current_frame = composite_frame
            
            detected_object_boxes, box_labels, _ = self.detect_objects_in_frame(current_frame)
            output_frame = self.draw_boxes_on_frame(current_frame, detected_object_boxes, box_labels)
            
            self.output_video_data.append(output_frame)
        
    def detect_objects_in_frame(self, frame):
        if self.frame_dimensions == None:
            self.frame_dimensions = frame.shape[:2][::-1]
        
        blob_ = cv2.dnn.blobFromImage(frame, 1 / 255, self.net_input_dims, swapRB=True)
        net_outputs = self.forward_through_net(blob_)
        bounding_boxes, class_labels, box_confidences = self.get_bounding_boxes(net_outputs)
        return bounding_boxes, class_labels, box_confidences
        
    def forward_through_net(self, blob):
        self.net.setInput(blob)
        layer_outputs = self.net.forward(self.layer_names)
        return layer_outputs
    
    def get_bounding_boxes(self, net_outputs):
        bounding_box_list, confidence_list, class_labels = self.extract_naive_boxes(net_outputs)
        boxes_metadata = {'confidences': confidence_list, 'labels':class_labels}
        nms_refactored_boxes, final_class_labels, confidences = self.extract_refactored_boxes(bounding_box_list, boxes_metadata)
        
        return nms_refactored_boxes, final_class_labels, confidences
        
    def extract_naive_boxes(self, output_list):
        boxes = []
        class_labels = []
        
        confidences = []

        for output in output_list:
            for detection in output:
                confidence_scores = detection[5:]
                predicted_class = np.argmax(confidence_scores)

                predicted_class_confd = confidence_scores[predicted_class]
                
                if predicted_class_confd > self.confidence_threshold:
                    original_width, original_height = self.frame_dimensions
                    rescaling_factor = [original_width, original_height, original_width, original_height]
                    
                    box = np.array(detection[:4] * np.array(rescaling_factor))
                    
                    box_centre_x, box_centre_y, box_width, box_height = box.astype("int")
                    top_left_corner_x = int(box_centre_x - 0.5 * box_width)
                    top_left_corner_y = int(box_centre_y - 0.5 * box_height)
                    
                    box = [top_left_corner_x, top_left_corner_y, box_width, box_height]
                    boxes.append(box)
                    class_labels.append(predicted_class)
                    confidences.append(predicted_class_confd)
                    
        return boxes, confidences, class_labels
    
    def extract_refactored_boxes(self, boxes, boxes_metadata):
        boxes = [np.array(box).astype(int) for box in boxes]
        confidences = [float(confidence) for confidence in boxes_metadata['confidences']]
        
        index_list = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)
        
        final_boxes = []
        final_class_labels = []
        final_confidence_list = []
        
        if len(index_list):
            for i in index_list.flatten():
                box_width, box_height = boxes[i][2], boxes[i][3]
                
                top_left_corner = boxes[i][0], boxes[i][1]
                bottom_right_corner = (top_left_corner[0] + box_width, top_left_corner[1] + box_height)
                
                box_details = [*top_left_corner, *bottom_right_corner]
                
                final_boxes.append(box_details)
                final_class_labels.append(boxes_metadata['labels'][i])
                final_confidence_list.append(confidences[i])
        
        return final_boxes, final_class_labels, final_confidence_list
    
    def draw_boxes_on_frame(self, frame, boxes, labels):
        for box, label in zip(boxes,labels):
            top_left_corner = tuple(box[:2])
            bottom_right_corner = tuple(box[2:])
            
            cv2.putText(frame, self.class_names[label], (top_left_corner[0]-50, top_left_corner[1]), cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,255), 1)
            cv2.rectangle(frame, top_left_corner, bottom_right_corner, (0, 0, 255), 2)
        
        return frame
        
    def output_processed_frames(self):
        return self.output_video_data
    
    def get_frame_rate(self):
        return self.frame_rate

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
        # print(frame_grabbed)
        if not frame_grabbed:
            break

        frame_list.append(current_frame)

    print(len(frame_list))

    objectD = ObjectDetectionModule(frame_list)
    objectD.process_rule()

    frames = objectD.output_processed_frames() # Return a list of output frames

    # out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 25, (640,360))
    
    # for frame in frames:
    #     out.write(frame)
    # out.release()
