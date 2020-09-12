# Backend Main Module

## Overview
The backend module processes the video and and returns video and screenshots to the frontend for display.

### Input
.mp4 video from user

### Output
.webm video and screenshots of traffic violations.

## Class Structure
A CompositeRuleObject, that acts like a pseudo factory method pattern, encloses all the rules, constructs their settings, and runs them. A VideoToFrame object converts the video into a list of frames, and gives it to the CompositeRuleObject, which in turn calls each object's process_rule, output_snapshots & output_processed_frames functions. The output frames are passed through a FrameToVideo object, which converts the frames into a video.
