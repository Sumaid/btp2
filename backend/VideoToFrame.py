import os
import cv2

class VideoToFrame:
    def __init__(self, file_name):
        self.file_name = file_name
        self.frame_list = []
        self.fps = 0
    
    def generate_frames_from_video(self):
        video_obj = cv2.VideoCapture(self.file_name)
        
        frame_number = 0
        
        number_of_frames = video_obj.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = video_obj.get(cv2.CAP_PROP_FPS)
        
        while frame_number < number_of_frames:
            frame_number += 1
            (frame_grabbed, current_frame) = video_obj.read()
            if not frame_grabbed:
                break

            self.frame_list.append(current_frame)

    def return_frame_data(self):
        return self.frame_list, self.fps
