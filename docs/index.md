# Welcome to Documentation

![Docs Status](https://readthedocs.org/projects/pip/badge/?version=latest&style=shields)

Full Code [Github Link](https://github.com/Sumaid/smart_traffic_analysis)

## Overview

Everyday a lot of accidents in the world happen due to the recklessness of drivers. Getting details immediately about the parties involved in the accident manually takes time. Hence, we propose using CCTV cameras and applying computer vision techniques in order to monitor traffic situations. Previous attempts at this have been restricted to one or two aspects of rule-breaking. We want to build a unified platform which will detect cars which don’t adhere to a set of rule-breaking aspects.

## Goals

Building a highly scalable web application with features to upload video or embed live stream directly to the application. Once the user uploads a video/opens the live stream to the platform, he can see the output video stream on the application.
The application will also capture photos of vehicles breaking following rules and store them in a database for future analysis. The app will be built such that it will be flexible to the addition of various other rules if required as well.
	The following scenarios will be taken care of by the app implemented in the project:
    
1. Vehicles should stop for pedestrians.
2. Vehicles should stop if the signal is red.
3. Vehicles should be under the speed limit.
4. Crash detection.

## Project layout

        backend/      # Flask application source code
        frontend/     # Angular application source code
        examples/     # Test videos with different features
        docker-compose.yml  # Yaml configuration file for docker compose
        README.md
        docs/
            mkdocs.yml    # Documentation Configuration File
            Project Anstract.pdf # Project Abstract
            Team1_design_doc.pdf # Design Document
            ...       # UI layouts, other images, etc.
            docs/
                index.md  # The documentation homepage.
                ...       # Other markdown files for documentation.
