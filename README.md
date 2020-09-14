# Smart Traffic Analysis


Presentation : [PPT](https://docs.google.com/presentation/d/1kDze7DhWdZDHkGL_AFtDGlgB0OhIKKMeBao2gsWz7cs/edit?usp=sharing)

Report : [Google Doc](https://docs.google.com/document/d/11iDqzZGAzez94tyzEA0_Ovs7kVi_bPORqTwjcQncoNY/edit?usp=sharing)

Code : [Github code link](https://github.com/Sumaid/btp2)

Documentation : [Github Pages Website](https://sumaid.github.io/btp2/)

Test Video Examples : [Google Drive Link](https://drive.google.com/drive/folders/10w9AgAyM6ImLYbiyJKuyXEGg-glvu6vw?usp=sharing)

## Overview

Everyday a lot of accidents in the world happen due to the recklessness of drivers. Getting details immediately about the parties involved in the accident manually takes time. Hence, we propose using CCTV cameras and applying computer vision techniques in order to monitor traffic situations. Previous attempts at this have been restricted to one or two aspects of rule-breaking. We want to build a unified platform which will detect cars which don’t adhere to a set of rule-breaking aspects.

## Goals

Building a highly scalable web application with features to upload video or embed live stream directly to the application. Once the user uploads a video/opens the live stream to the platform, he can see the output video stream on the application.
The application will also capture photos of vehicles breaking following rules and store them in a database for future analysis. The app will be built such that it will be flexible to the addition of various other rules if required as well.
	The following scenarios will be taken care of by the app implemented in the project::
1. Vehicles should stop for pedestrians.
2. Vehicles should stop if the signal is red.
3. Vehicles should be under the speed limit.
4. Crash detection.

# Building the application

## Clone/Fork repository

First fork or clone this repo:

e.g. `git clone https://github.com/Sumaid/sta.git`
 
 Download [Weights file](https://pjreddie.com/media/files/yolov3.weights) and place it in `backend/yolo_files/`

## Build images and run containers with docker-compose

Install [Docker Desktop](https://docs.docker.com/get-docker/).

After cloning the repository go inside the project folder:

`cd sta`

Run `docker-compose up --build` which will start a Flask web application for the backend API (default port `8081`) and an Angular frontend served through a webpack development web server (default port `4200`).
Few things to keep in mind:
1. If you want to run docker-compose in background use -b flag.
2. If your one part crashes like if backend crashes, then you can simply fix the issue and run `docker-compose restart backend` in a different terminal to get that part running.
Similar if frontend crashes, just run `docker-compose restart frontend`.

## Access your app

In your browser navigate to: `http://localhost:4200` (or whatever port you defined for the frontend in `docker-compose.yml`).

For testing your backend API I recommend using [Postman](https://www.getpostman.com/) or Curl, but you can also go to `http://localhost:8081/api` ( if you are just testing simple GET requests ).
  

## Working __without__ docker 

I highly recommend the use of docker and docker-compose as it is far simpler to get started. The great thing about docker is you can run one command `docker-compose up` on any operating system & environment and your application will be up and running!
But still if you want to work without docker, you can go through following steps:

### Backend development

Navigate inside the backend directory: `cd backend`

Install pip dependencies: `pip3 install -r requirements.txt`

Run `python3 app.py` in backend root (will watch files and restart server on port `8081` on change).

### Frontend development

Navigate inside the frontend directory: `cd frontend`

Assure you have [Nodejs](https://nodejs.org/en/) installed.

Run following commands: 
1. `rm -rf node_modules dist tmp` 
2. `npm install --save-dev angular-cli@latest`
3. `npm install`
4. `npm init`

Run `ng serve --host 0.0.0.0 --disableHostCheck --proxy-config proxy.conf.json` in frontend root (will watch files and restart dev-server on port `4200` on change).
All calls made to `/api` will be proxied to backend server (default port for backend `8081`), this can be changed in `proxy.conf.json`.

## Things to keep in mind

1. You can change port numbers in `docker-compose.yml`, but if you change backend port number, 
keep in mind to change it in `frontend/proxy.conf.dev.json` also.
2. If you add new requirements, rerun the command `docker-compose up`.
3. Each api route in backend should have base `/api/`, so create apis in the format, `/api/yourroute/`.
4. For any new feature, create a new branch & PR before merging it into master.