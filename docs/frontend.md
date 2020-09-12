# Frontend

## Overview 

Angular ( TypeScript ) framework is used for frontend of the application. We have written code in a modular way, segregating different parts into following components.

1. App root component
2. Input Video component
3. Video Streaming component
4. Snapshots Rendering component
5. Radio buttons component

## App root component

Main component of the framework. 

### Objectives 

1. Keep Track of state of the application.
2. Manage global state of the application.

### Functions 

1. `refreshEvent(event)` :
    * Input : Feature Type wrapped in an Angular Event
    * Trigger : User clicking a different feature type will trigger this function
    * Function : Reloading video stream and snapshots based on selected feature
    * Output : None

2. `stateOff(event)` :
    * Input : Application state wrapped in an Angular Event
    * Trigger : Backend processing getting completed
    * Function : Changing application state at global level
    * Output : None

### Variables

1. `state` :
    * Type : Boolean ( True / False )
    * Purpose : Global application state indicating whether media files should be rendered or not
    * Default Value : `false`

2. `title` : 
    * Type : String
    * Purpose : Title of the application
    * Default Value : `frontend`

### Modules

1. `@angular/core/ViewChild` :
    * Purpose : To access video streaming and snapshots components from typescript code.

## Input Video Component

### Objectives

1. Take user's video as input and send it to backend
2. Once user selects video, ask users for different parameters which will be used in analysis
3. Send parameters to backend for analysis

### Functions

1. `startProcessing()` :
    * Input : None
    * Trigger : User clicking 'Start' button 
    * Purpose : To set the application status to 'processing'
    * Output : None

2. `finishProcessing()`:
    * Input : None
    * Trigger : Backend finishing processing
    * Purpose : To set the application status to done with processing
    * Output : None

3. `upload()`:
    * Input : None
    * Trigger : User clicking upload button
    * Purpose : To upload video to backend
    * Output : None

3. `getImage()`:
    * Input : Image url ( String )
    * Trigger : User starting process of uploaded video
    * Purpose : To get a frame of video on which user can draw
    * Output : None

4. `openModal(templateReference)`:
    * Input : Reference to a modal box tag in template
    * Trigger : User clicking next on modal boxes
    * Purpose : Open the corresponding modal box
    * Output : None

5. `saveRoadLength(input_)`:
    * Input : Reference to input tag in template
    * Trigger : User clicking next after typing road length
    * Purpose : Save the typed road length input
    * Output : None

6. `loadCanvas(modalName)`:
    * Input : Name of modal box
    * Trigger : User wanting to draw on image
    * Purpose : Load canvas on top of image on which user can draw
    * Output : None

7. `btnClick()`:
    * Input : None
    * Trigger : Finishing inputting parameters
    * Purpose : Finishing inputting parameters
    * Output : None

8. `finalize()`:
    * Input : None
    * Trigger : User clicking 'Next' button in the last modal box
    * Purpose : Finalize parameters
    * Output : None

9.  `makePolygon()`:
    * Input : None
    * Trigger : User clicking 4th point in the drawing
    * Purpose : Making polygon out of selected points
    * Output : None

10. `clearCanvas()`:
    * Input : None
    * Trigger : User finishing drawing
    * Purpose : Clear drawing canvas
    * Output : None

11. `diableButtonsOnClearCanvas()`:
    * Input : None
    * Trigger : User clicking buttons on canvas
    * Purpose : Disable buttons on clear canvas selection
    * Output : None

12. `getCoordinatesZebra()`:
    * Input : None
    * Trigger : User clicking next on zebra crossing modal box
    * Purpose : To save coordinates of zebra corssing
    * Output : None

13. `getCoordinatesPedestrian()`:
    * Input : None
    * Trigger : User clicking next on pedestrian modal box
    * Purpose : To save coordinates of pedesitrian area
    * Output : None

12. `getCoordinatesLane()`:
    * Input : None
    * Trigger : User clicking next on lane marking modal box
    * Purpose : To save coordinates of lane markings
    * Output : None

### Variables

1. `uploadedFiles` :
    * Type : Array<'File'>
    * Purpose : Store uploaded files
    * Default Value : Empty

2. `state` : 
    * Type : Boolean 
    * Purpose : State of the application
    * Default Value : Same as root component

3. `processingStatus` : 
    * Type : Boolean
    * Purpose : Stores whether processing is completed or not
    * Default Value : `false`

4. `stateOff` : 
    * Type : Event Emitter
    * Purpose : To trigger parent component to change status
    * Default Value : `false`

5. `uploadStatus` : 
    * Type : Boolean
    * Purpose : To show whether uploading is done or not
    * Default Value : `false`

6. `scalingFactorX` : 
    * Type : Float
    * Purpose : To show how much to scale coordinates in x direction
    * Default Value : `1`

7. `scalingFactorY` : 
    * Type : Float
    * Purpose : To show how much to scale coordinates in y direction
    * Default Value : `1`

8. `uploaded` : 
    * Type : Boolean
    * Purpose : To show status about uploading
    * Default Value : `false`

9. `imageToShow` : 
    * Type : any
    * Purpose : Image which will be showed
    * Default Value : None

10. `isImageLoading`:
    * Type : any
    * Purpose : To store status of image loading
    * Default Value : None

11. `fileName` :
    * Type : String
    * Purpose : To store filename of uploaded video
    * Default Value : Empty String

12.  `uploadDisabled` : 
    * Type : Boolean
    * Purpose : To show whether upload button is disabled or not
    * Default value : `false`

13. `fileSize` : 
    * Type : Integer
    * Purpose : To store size of file
    * Default value : 0

14. `inputSpeedForm` :
    * Type : FormGroup
    * Purpose : Form for taking speed limit as input
    * Default value : None

15. `roadLendthForm` : 
    * Type : FormGroup
    * Purpose : Form for taking road length as input
    * Default value : None

16. `speedlimit` : 
    * Type : Integer
    * Purpose : Speedlimit 
    * Default Value : 100

17. `roadLendth` : 
    * Type : Integer
    * Purpose : To store approximate lenght of road in metres
    * Default Value : 0


### Modules

1. `@angular/common/http` :
    * Purpose : To make HTTP requests including posting videos and parameters

2. `rxjs/operators` : 
    * Purpose : To extend timeout period of HTTP requests to ensure that 

## Video Streaming Component

### Objectives 

1. Render video from backend onto frontend
2. Reload appropriate video based on feature selected

### Functions

1. `reload(feature)`:
    * Input : Rule breaking feature selected
    * Trigger : User clicking radio button of a traffic rule feature
    * Purpose : To change the video based on traffic rule selected
    * Output : None

### Variables

1. `videoelement` : 
    * Type : HTMLVideoElement
    * Purpose : Based on feature selected, reloading video
    * Default Value : None

2. `base` : 
    * Type : String
    * Purpose : Base url from where to retrieve video
    * Default Value : '/api/getvideo/'

3. `url` :
    * Type : String
    * Purpose : Final url from where to retrieve video
    * Default Value : '/api/getvideo/'

4. `state` : 
    * Type : Boolean
    * Purpose : Global application state binded to parent, to show whether to render application or not
    * Default Value : Same as Parent

### Modules

1. `@angular/core/Input` :
    * Purpose : To bind a variable to parent component variable

## Snapshots Rendering Component

### Objectives 

1. Retrieve images corresponding to a particular feature
2. Render images with a scrollbar

### Functions 

1. `reload(feature)`:
    * Input : Rule breaking feature selected
    * Trigger : User clicking radio button of a traffic rule feature
    * Purpose : To change the images based on traffic rule selected
    * Output : None

### Variables

1. `imagesList` :
    * Type : Array
    * Purpose : To store list of images to render on the component
    * Default Value : Empty Array

2. `feature` : 
    * Type : String
    * Purpose : Global variable to store feature, corresponding to that feature images will be rendered
    * Default Value : 'default'

3. `state` : 
    * Type : Boolean
    * Purpose : Global application state binded to parent, to show whether to render images or not
    * Default Value : Same as Parent

### Modules

1. `@angular/common/http` :
    * Purpose : To make HTTP request to retrieve images from backend

## Radio buttons component

### Objectives

1. Provide user with radio buttons for easy navigation between different features
2. Based on radio button selected reload video streaming and rendering snapshots

### Functions

1. `handleClick(event)`:
    * Input : Rule breaking feature selected wrapped in an event
    * Trigger : User clicking radio button of a traffic rule feature
    * Purpose : To invoke reload functions in snapshot and video components
    * Output : None


### Variables

1. `refreshEvent` :
    * Type : EventEmitter
    * Purpose : Event Emitter, binded with parent
    * Default Value : None

2. `feature` : 
    * Type : String
    * Purpose : Global variable to store feature, that feature will be passed to snapshots and video components
    * Default Value : 'default'

3. `state` : 
    * Type : Boolean
    * Purpose : Global application state binded to parent, to show whether to render images/video or not
    * Default Value : Same as Parent

### Modules

1. `@angular/common/http` :
    * Purpose : To make HTTP request to retrieve images from backend

2. `@angular/core/EventEmitter` :
    * Purpose : Binding variables from parent to child components