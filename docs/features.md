# Backend Features

There are 4 submodules corresponding to different traffic violation detection.

1. Car Crash Detection
2. Overspeeding Detection
3. Pedestrians Detection
4. Traffic Signal Detection

## Car Crash Detection

### Overview 
This module finds crashes / accidents among Cars, Trucks, Bus, Person.
Class takes a list of frames passed on from the Object Detection Module as input and saves screenshot of crashes into another folder.

### Objectives 

1. Identify crashes between various objects.
2. Identify the objects involved in crashes and highlight them.
2. Store the screenshots of frames that have crashes in them.

### Class

1. CrashDetectionModule
    * Input : List of frames
    * Function : Detects and stores crashes for a given video
    
### Functions 

1. `process_rule()` :
    * Input : None
    * Function : Driver function having all major function calls. Takes each frame, sends it to object detection module and then detects crash.
    * Output : None

2. `detect_crash(current_frame, boxes, box_labels)` :
    * Input : current_frame(frame object) to be processed along with the bounding boxes (list of list) present and their box_labels (list)
    * Trigger : Called by process_rule()
    * Function : Main crash computation function. 
    * Output : None


3. `get_crash_objects_list(box_labels)` :
    * Input : box_labels(list) - labels of the detected objects
    * Trigger : Called by detect_crash(...)
    * Function : Saves the indexes of all the objects whose crash we are interested in. 
    * Output : crashObjects(list)
    
4. `get_overlap_variables(box)` :
    * Input : box(list) - top left and bottom right coordinates of the object
    * Trigger : Called by detect_crash(...)
    * Function : Computes the coordinates of the center of object and it's height and width.
    * Output : (list) of coordinates of center and objects bounding box's height and width.


5. `detect_overlap(object1_carsh_variables, object2_crash_variables)` :
    * Input : object1_carsh_variables and object2_crash_variables list returned by the get_overlap_variables(...) function
    * Trigger : Called by detect_crash(...)
    * Function : Computes if there is a collision between two objects.
    * Output : (boolean) to indicate if there is a collision or not
 
6. `report_crash(frame, crashing_objects)` :
    * Input : frame(frame object) is the current frame and crashing_objects(list of list) consists of the coordinates of the bounding boxes of the two objects involved in crash
    * Trigger : Called by detect_crash(...) when detect_overlap(...) return True
    * Function : Driver function that increments the counts of total crashes call the box drawing function and the save_screenshot(...) function.
    * Output : None
    
7. `draw_crashing_objects(frame, crashing_objects)` :
    * Input : frame(frame object) is the current frame and crashing_objects(list of list) consists of the coordinates of the bounding boxes of the two objects involved in crash
    * Trigger : Called by report_crash(...)
    * Function : Highlights the objects whose crash takes place
    * Output : frame(frame object) the modified frame which has the highlighted crashing objects

8. `add_snapshot(frame)` :
    * Input : frame(frame object) is the current frame
    * Trigger : Called by detect_crash(...)
    * Function : Increments the total number of crashes and stores the crash frame
    * Output : None
    
9. `output_snapshot()` :
    * Input : None
    * Trigger : -
    * Function : Saves the screenshots of crashes into a folder
    * Output : None


### Variables

1. `total_crashes` :
    * Type : Int
    * Purpose : Stores the total number of crashes for the current frame
    * Default Value : 0

2. `frame_saved` : 
    * Type : Int
    * Purpose : Frame number of the last frame whose screentshot was saved
    * Default Value : -100


3. `current_frame_num` : 
    * Type : Int
    * Purpose : Frame number of the frame whose screentshot is saved
    * Default Value : -1
    
    
4. `objects_to_monitor` : 
    * Type : List
    * Purpose : Stores the index of all the objects whose crash we are interested in. (Indexes are stored according to the coco.names file)
    * Default Value : [0, 2, 5, 7]
    * NOTE : Refer  [coco.names](https://github.com/pjreddie/darknet/blob/master/data/coco.names) file to add more objects 
      
    
5. `inverse_collision_relaxation_x` : 
    * Type : Float
    * Purpose : One minus this fraction allows how much one object can be inside another object along x and still collision will be detected
    * Default Value : 0.9
    

6. `inverse_collision_relaxation_y` : 
    * Type : Float
    * Purpose : One minus this fraction allows how much one object can be inside another object along y and still collision will be detected
    * Default Value : 0.6


7. `input_video_data` : 
    * Type : List
    * Purpose : Contains the frames of the input video

8. `output_video_data` : 
    * Type : List
    * Purpose : Contains the modified frames
    * Default Value : []
    
### Modules

Following is the list of modules used for this feature.

1. `objectDetectionModule` :
    * Purpose : Returns all the objects in the frame along with thier labels for crash detection.

2. `opencv` :
    * Purpose : Used for highlighting objects

### Workflow and Logic

*__init__()* Initializes the variables then *process_rule()* takes input video data and then for each frame detects crash.
*detect_crash()* then takes current frame, it’s detected objects and those object labels. First it finds out all the objects whose accident/crash we are interested in using the *get_crash_objects_list()* function. Ex car, person, bus etc. Next it gets the coordinates which are used for collision detection from the *get_overlap_variables()* function.
After getting these *detect_overlap()* checks if there is a collision. If there is the objects are passed onto the function *report_crash()* which in turn calls the rectangle drawing function *draw_crashing_objects()*  and the *save_screenshot()* function to store the frame’s screenshot.

## Overspeeding

### Overview 
The overspeeding module checks if there are any cars that are overspeeding on the marked lane

### Objectives 

1. To detect overspeeding cars on the lane
2. To save screenshots of the overspeeding cars

### Functions 

1. `process_rule` :
    * Input : frames of video
    * Trigger : External trigger from composite object
    * Function : Tracks cars in the lane and checks the speed by calculating the time taken to cover the lane distance
    * Output : None, just calls relevant functions to perform actions in case of overspeeding

2. `check_line_intersection` :
    * Input : two lines, which are each a tuple of tuples
    * Trigger : called for the process_rule to see if a car has crossed the start/end line
    * Function : to find if the two lines have intersected
    * Output : returns a boolean value depending on whether the lines have intersected or not

3. `calculate_speed` :
    * Input : number of frames taken for a bounding box to cross the lane 
    * Trigger : called to check speed of the car
    * Function : to calculate the actual speed of the car
    * Output : returns the speed of the vehicle

4. `add_snapshot` :
    * Input : current frame, the boundng box coordinates of the car, speed of the car, and current frame number
    * Trigger : called when the car exceeds the speed limit
    * Function : to add snapshot details of a violating car to a list
    * Output : appends a snapshot to the list

3. `output_snapshots` :
    * Input : none
    * Trigger : Called from external module
    * Function : saves the snapshots taken
    * Output : Saves snapshots in the format speed_timeofvideo_randomstring.jpg
### Variables

The generic metadata have been loaded as variables, as a start and end line for measuring speed, a tracker to keep track of the SORT results, and a snapshoot details array.

### Logic

The overspeed detection module is one of the traffic rule violation detection modules. The user marks the zone in which the over speed detection should take place – by marking a rectangle in the front end. This sends back the co-ordinates of the edges of the zone to this module. Also the user enters the road length for the marked speed detection zone.
This module uses the object detection algorithm and the SORT Algorithm to detect and track objects across the frames of the video (in future CCTV frames). Once the object detected (box) crosses the start and end edges of the speed detection zone the speed of the object is calculated using the following formula:

3.6 * frame rate * road distamce/ frames taken by the car to cross the lines

If the speed is within the speed limit, no action is taken. Once the speed exceeds the speed limit entered by the user, the object is marked in RED and the screenshot is saved in the prescribed folder.

    
### Modules

Following is the list of modules used for this feature.

1. `objectDetectionModule` :
    * Purpose : Returns all the objects in the frame
2. `opencv` :
    * Purpose : Used for highlighting objects
    
3. `SORT`:
    * Purpose: to track the object across frames 

## Yield for Pedestrians Detection

### Overview 
This module finds Cars, Trucks, Buses or Motorcycles which enter Pedestrian area while it's still in use for crossing.
Class takes a list of frames passed on from the Object Detection Module as input and saves screenshot of violations into another folder.

### Objectives 

1. Identify vehicles which violate Pedestrian Crossing.
2. Store the screenshots of frames that have violations in them.

### Functions 

1. `process_rule` :
    * Input : None
    * Trigger : External trigger from composite object
    * Function : Driver function having all major function calls. Takes each frame, sends it to object detection module and then detects any violations.
    * Output : None
    
2. `draw_pedestrian_boxes` :
    * Input : frame(frame object) to be processed along with the waiting_boxes (list of list) and
    crossing_boxes(List of List) obtained from *assign_pedestrian_boxes()* 
    * Trigger : Called by process_rule()
    * Function : Highlights the waiting and crossing areas
    * Output : frame(frame object)
   
3. `detect_violation` :
    * Input : frame(frame object) to be processed along with the bounding boxes (tuple of list of list) present and their labels (list) 
    * Trigger : Called by process_rule()
    * Function : Detects if a vehicle does not stop when pedestrians are waiting to cross the road or are already crossing the road
    * Output : None
    
4. `object_in_box` :
    * Input : obj(list) contains coordinates of the the object and box(list) contains coordinates of the box 
    * Trigger : Called by detect_violation()
    * Function : Detects if the object is inside the box
    * Output : (boolean) to indicate if the object is inside the box or not
  
5. `draw_violating_objects` :
    * Input : frame(frame object) is the current frame and crashing_objects(list of list) consists of the coordinates of the bounding boxes of the two objects involved in violation (vehicle and person)
    * Trigger : Called by detect_violation()
    * Function : Highlights the vehicles that violate rules
    * Output : frame(frame object) the modified frame which has the highlighted violating objects
   
6. `add_snapshot` :
    * Input : frame(frame object) is the current frame
    * Trigger : Called by detect_violation()
    * Function : Saves a screenshot of the violation frame
    * Output : None
    
7. `output_snapshots` :
    * Input : None
    * Trigger : External trigger from composite object
    * Function : Saves the screenshots of violations into a folder
    * Output : None
    
9. `set_metadata(metadata)` :
    * Input : metadata (dict)
    * Trigger : External trigger from composite object
    * Function : Loads the meta data
    * Output : None
    
### Variables

1. `num_violations` :
    * Type : Int
    * Purpose : Stores the total number of violations in the video
    * Default Value : 0

2. `frame_saved` : 
    * Type : Int
    * Purpose : Frame number of the last frame whose screentshot was saved
    * Default Value : -100

3. `current_frame_num` : 
    * Type : Int
    * Purpose : Frame number of the frame currently being processed
    * Default Value : -1

4. `waiting_boxes` :
    * Type : List of List
    * Purpose : Stores the coordinates of the pedestrian waiting areas
    * Default Value : []

5. `crossing_boxes` :
    * Type : List of List
    * Purpose : Stores the coordinates of the zebra crossing areas
    * Default Value : []

6. `vehicle_list` : 
    * Type : List
    * Purpose : Stores names of vehicle whose violations need to be kept track of
    * Default Value : ['motorbike', 'bus', 'truck', 'car']

7. `input_video_data` : 
    * Type : List
    * Purpose : Contains the frames of the input video
    * Default Value: []

8. `output_video_data` : 
    * Type : List
    * Purpose : Contains the modified frames
    * Default Value : []
    
### Modules

Following is the list of modules used for this feature.

1. `objectDetectionModule` :
    * Purpose : Returns all the objects in the frame along with their labels for crash detection.

2. `opencv` :
    * Purpose : Used for highlighting objects

### Logic

We check if there is a pedestrian either waiting to cross the road or already crossing the road. Next we check if any vehicles do not stop for the pedestrians to cross the road. This is done by checking if a given object is in the box area defined as pedestrian area. If there is a violation, the vehicles violating the rule are highlighted and a screenshot is saved.

## Stop for Traffic Signal Detection

### Overview 
This module finds Cars, Trucks, Buses or Motorcycles which break Traffic Signals.
Class takes a list of frames passed on from the Object Detection Module as input and saves screenshot of violations into another folder.

### Objectives 

1. Identify vehicles which violate Traffic Signals.
2. Store the screenshots of frames that have violations in them.

### Functions 

1. `process_rule` :
    * Input : None
    * Trigger : External trigger from composite object
    * Function : Driver function having all major function calls. Takes each frame, sends it to object detection module and then detects any violations.
    * Output : None

2. `simulate_signal` :
    * Input : None
    * Trigger : process_rule()
    * Function : Simulates a traffic signal
    * Output : signal(list)
    
3. `draw_traffic_box(frame)` :
    * Input : frame(frame object) to be processed 
    * Trigger : Called by process_rule()
    * Function : Highlights the traffic stop area for signals
    * Output : frame(frame object)
    
4. `detect_violation` :
    * Input : frame(frame object) to be processed along with the bounding boxes (list of list) present and their labels (list) 
    * Trigger : Called by process_rule()
    * Function : Detects if there is a vehicle outside the traffic box
    * Output : None
    
5. `object_in_box` :
    * Input : obj(list) contains coordinates of the the object and box(list) contains coordinates of the box 
    * Trigger : Called by detect_violation()
    * Function : Detects if the object is inside the box
    * Output : (boolean) to indicate if the object is inside the box or not
  
6. `draw_violating_objects(frame, violating_objects)` :
    * Input : frame(frame object) is the current frame and violating_objects(list of list) consists of the coordinates of the bounding boxes of vehicles that come out of the traffic box
    * Trigger : Called by detect_violation()
    * Function : Highlights the vehicles that violate rules
    * Output : frame(frame object) the modified frame which has the highlighted violating objects
    
7. `add_snapshot(frame)` :
    * Input : frame(frame object) is the current frame
    * Trigger : Called by detect_violation()
    * Function : Increments the total number of violations and stores the violation frame
    * Output : None
    
8. `output_snapshot()` :
    * Input : None
    * Trigger : External trigger from composite object
    * Function : Saves the screenshots of violations into a folder
    * Output : None

9. `set_metadata(metadata)` :
    * Input : metadata (dict)
    * Trigger : External trigger from composite object
    * Function : Loads the meta data
    * Output : None

    
### Variables

1. `num_violations` :
    * Type : Int
    * Purpose : Stores the total number of violations for the current frame
    * Default Value : 0
    
2. `frame_saved` : 
    * Type : Int
    * Purpose : Frame number of the last frame whose screentshot was saved
    * Default Value : -100

3. `current_frame_num` : 
    * Type : Int
    * Purpose : Frame number of the frame whose screentshot is saved
    * Default Value : -1

4. `traffic_box` :
    * Type : List 
    * Purpose : Stores the coordinates of the traffic box
    * Default Value : []

5. `crossing_boxes` :
    * Type : List of List
    * Purpose : Stores the coordinates of the crossing areas
    * Default Value : []

6. `vehicle_list` : 
    * Type : List
    * Purpose : Stores names of vehicle whose violations need to be kept track of
    * Default Value : ['motorbike', 'bus', 'truck', 'car']
    
7. `input_video_data` : 
    * Type : List
    * Purpose : Contains the frames of the input video
    * Default Value : []

8. `output_video_data` : 
    * Type : List
    * Purpose : Contains the modified frames
    * Default Value : []
    
### Modules

Following is the list of modules used for this feature.

1. `objectDetectionModule` :
    * Purpose : Returns all the objects in the frame along with thier labels for crash detection.

2. `opencv` :
    * Purpose : Used for highlighting objects

### Logic

We keep track of the all the vehicles coordinates and if it steps out traffic box then we detect a violation. For this, we check if the rectangle defining a vehicle and the traffic box are overlapping.

