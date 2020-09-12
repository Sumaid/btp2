# Building the application

## Clone/Fork repository

First fork or clone this repo:

e.g. `git clone https://github.com/Sumaid/smart_traffic_analysis.git`
 

## Build images and run containers with docker-compose

Install [Docker Desktop](https://docs.docker.com/get-docker/).

After cloning the repository go inside the project folder:

`cd smart_traffic_analysis`

Run `docker-compose up` which will start a Flask web application for the backend API (default port `8081`) and an Angular frontend served through a webpack development web server (default port `4200`).
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

### Documentation development

Run following commands in root directory of project: 

1. `pip3 install mkdocs mkdocs-material` 
2. `mkdocs serve` 

Documentation will be hosted locally at [http://0.0.0.0:8000](http://0.0.0.0:8000). Host can be changed in `mkdocs.yml`.
Documentation is also publicly hosted at [https://sumaid.github.io/smart_traffic_analysis/](https://sumaid.github.io/smart_traffic_analysis/).

If you make any changes in documentation, test it with `mkdocs serve` then 

1. Push changes to remote repository
2. Run `mkdocs gh-deploy` to deploy changes to publicly hosted documentation


## Things to keep in mind

1. You can change port numbers in `docker-compose.yml`, but if you change backend port number, 
keep in mind to change it in `frontend/proxy.conf.dev.json` also.
2. If you add new requirements, rerun the command `docker-compose up`.
3. Each api route in backend should have base `/api/`, so create apis in the format, `/api/yourroute/`.
4. For any new feature, create a new branch & PR before merging it into master.