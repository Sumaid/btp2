# Backend Server

## Overview

Flask is used as the backend server for creating APIs and processing videos on backend.

## APIs

1. `/api` : 
    * Type : GET, POST
    * Input : None
    * Purpose : Render flask home
    * Output : Flask home HTML

2. `/api/postvideo` :
    * Type : POST
    * Input : Video File
    * Purpose : To save video file recieved from front end
    * Output : Success/Error Status

3.  `/api/getframe/filename` : 
    * Type : GET
    * Input : Video file name
    * Purpose : To send frame of video to frontend
    * Output : Frame of vide

4. `/api/postparameters` : 
    * Type : POST
    * Input : Parameters corresponding to different violation principles
    * Purpose : To send parameters to backend which will be used in processing
    * Output : Success/Error Status

5. `/api/imageslist/feature` : 
    * Type : GET
    * Input : Featue Type
    * Purpose : Depending on feature selected, return list of images corresponding to that feature
    * Output : List of images which can later be retrieved by frontend

6. `/api/getimage` : 
    * Type : Get
    * Input : None
    * Purpose : Return a sample iamge
    * Output : Sample Image

7. `/api/getvideo/feature` : 
    * Type : GET
    * Input : Feature Type
    * Purpose : Get partial response of video in chunks
    * Output : Partial Response



## Functions

1. `cleanMedia()` : 
    * Input : None
    * Purpose : To clean all the media files from previous processing
    * Output : None

2. `createDirectories()` :
    * Input : None
    * Purpose : To create feature directories for runtime purposes
    * Output : None

## Modules

1. `video_stream` 
    * In house implemented video streaming server. 
    * Instead of returning entire video at once, it is returned in chunks which are rendered on browser

2. `cv2`:
    * Opencv helps in retrieving frame from a video which user can draw on

