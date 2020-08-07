class RuleProcessor:
    def __init__(self, inputVideo = None):
        self.input_video_data = inputVideo # frame from the video processing object
        self.output_video_data = None
        self.snapshot_data = []  # List of snapshot data
        self.frame_dimensions = None
    
    def set_frame_rate(self, frame_rate):
        self.frame_rate = frame_rate

    def get_frame_rate(self):
        return self.frame_rate
        
    def get_frame_dimensions(self):
        return self.frame_dimensions
    
    def process_rule(self):
        pass
    
    def output_processed_frames(self):
        return self.output_video_data
    
    def output_snapshots(self):
        pass
    
    def set_metadata(self, metadata):
        pass
