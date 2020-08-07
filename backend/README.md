# Flask backend API

You can build Flask backend using any one of the following two ways.

## Development server

Run `python3 app.py 8081` to start development server on port `8081` to watch files and restart on update.

## Use from docker container

Clone project on your remote machine (needs to have docker daemon installed), then build image (`docker build -t flask-backend .`) and finally run the image by using `docker run -p 8081:8081 -v /HOST/PATH/TO/BACKEND/FOLDER:/app flask-backend`.

## Things to keep in mind
1. Feature folders with images and video will be created and deleted in runtime.
2. It will follow directory structure : 

        default/      # Folder with default object detection outputs
            images/ # Snapshots corresponding to this particular feature
            video/ # Video with this particular feature detected
        crash/     # Crash detection 
            images/ 
            video/ 
        overspeed/     # Detect overspeeding vehicles
            images/ 
            video/ 
        pedestrian/     # Detect vehicles not stopping for pedestrians 
            images/ 
            video/ 
        trafficsignal/     # Detect vehicles breaking traffic signal
            images/ 
            video/ 
