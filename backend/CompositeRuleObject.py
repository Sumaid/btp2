import os
from ObjectDetectionModule import ObjectDetectionModule

from PedestrianModule import PedestrianModule
from OverspeedingModule import OverspeedingModule
from CrashDetectionModule import CrashDetectionModule
from TrafficSignalModule import TrafficSignalModule

from VideoToFrame import VideoToFrame
from FrameToVideo import FrameToVideo

import numpy as np

class CompositeRuleObject:
    def __init__(self, metadata, frame_list, fps):
        self.video_frames = frame_list
        self.video_fps = fps
        
        self.rule_dict = {
            'default': ObjectDetectionModule(np.array(frame_list)),
            'crash': CrashDetectionModule(np.array(frame_list)),
            'overspeed': OverspeedingModule(np.array(frame_list)),
            'pedestrian': PedestrianModule(np.array(frame_list)),
            # 'trafficsignal': TrafficSignalModule(frame_list)
        }
        
        self.metadata = metadata

    def build_rule(self, rule_object):
        print(self.metadata)
        rule_object.set_frame_rate(self.video_fps)
        rule_object.set_metadata(self.metadata)
        return rule_object

    def rule_list_constructor(self):
        rule_list = []
        for rule_processor in sorted(self.rule_dict.keys()):
            built_rule = self.build_rule(self.rule_dict[rule_processor])
            rule_list.append(built_rule)
        
        return rule_list
    
    def process_rules(self):
        self.rule_list = self.rule_list_constructor()
        rule_list_strings = sorted(self.rule_dict.keys())
        
        for rule in self.rule_list:
            rule.process_rule()

    def save_videos(self):
        rule_names = sorted(self.rule_dict.keys())
        
        for rule, rule_name in zip(self.rule_list, rule_names):
            output_frames = rule.output_processed_frames()
            frame_to_video_converter = FrameToVideo(output_frames, self.video_fps)
            
            frame_to_video_converter.save_video(rule_name)
    
    def save_snapshots(self):
        rule_names = sorted(self.rule_dict.keys())
        
        for rule, rule_name in zip(self.rule_list, rule_names):
            rule.output_snapshots()

# if __name__ == '__main__':
#     inputfilename = "cars2.mp4"

#     metadata = {
#     'speed_limit': 20,
#     'lane_data': [[195.84,165.6],[577.28,163.44],[572.16,158.4],[200.96,161.28]],
#     'zebra_crossing': [[668.16,200.16],[716.8000000000001,221.76],[652.8000000000001,257.76],[555.52,230.39999999999998]],
#     'pedestrian_area': [[552.96,249.12],[564.48,194.4],[628.48,223.92],[628.48,244.07999999999998]],
#     'road_length': 200
#     }

#     video_frame_convertor = VideoToFrame(inputfilename)
#     video_frame_convertor.generate_frames_from_video()
#     video_frames, fps = video_frame_convertor.return_frame_data()

#     composite_rule_object = CompositeRuleObject(metadata, video_frames, fps)
#     composite_rule_object.process_rules()
#     composite_rule_object.save_videos()
#     composite_rule_object.save_snapshots()
