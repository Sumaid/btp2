import os
import cv2


class FrameToVideo:
    def __init__(self, frames, frame_rate):
        self.frames = frames
        self.frame_rate = frame_rate
        self.frame_dimensions = (
            self.frames[0].shape[1], self.frames[0].shape[0])

    def save_video(self, feature_name):
        out = cv2.VideoWriter(feature_name + '/video/output.webm',
                         cv2.VideoWriter_fourcc('V','P','8','0'), self.frame_rate, self.frame_dimensions)

        for frame in self.frames:
            out.write(frame)
        out.release()
