from __future__ import print_function

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import logging
import os
import cv2
import re
import sys
import time
import json
import pprint
import glob
from datetime import datetime
import requests

import mimetypes
from flask import Response, render_template
from flask import jsonify
from flask import send_file, send_from_directory
from flask import request,Flask

from CompositeRuleObject import CompositeRuleObject
from VideoToFrame import VideoToFrame
from FrameToVideo import FrameToVideo

from video_stream import partial_response, get_range
from werkzeug.utils import secure_filename

from flask_cors import CORS, cross_origin

LOG = logging.getLogger(__name__)
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
PORT = int(os.getenv('PORT')) if os.getenv('PORT') else 8081
HOST = '0.0.0.0'
MB = 1 << 20
BUFF_SIZE = 10 * MB

processingDone = False
inputfilename = ''

rule_list = ['crash','default','overspeed','pedestrian','trafficsignal']

@app.route('/')
@cross_origin()
def rootApi():
    return 'Hi there!, Please make sure every route starts with /api/'

@app.route('/api')
@cross_origin()
def baseApi():
    return 'Hello, World! ( Flask Backend App )'

def cleanMedia():
    global processingDone
    processingDone = False
    files = glob.glob("*.mp4")+glob.glob("*.jpg")+\
        glob.glob("./crash/images/*")+glob.glob("./crash/video/*")+\
        glob.glob("./default/images/*")+glob.glob("./default/video/*")+\
        glob.glob("./overspeed/images/*")+glob.glob("./overspeed/video/*")+\
        glob.glob("./pedestrian/images/*")+glob.glob("./pedestrian/video/*")+\
        glob.glob("./trafficsignal/images/*")+glob.glob("./trafficsignal/video/*")
    for fil in files:
        os.remove(fil)

def createDirectories():
    for dr in rule_list:
        if not dr in os.listdir('./'):
            os.mkdir(dr)
        if not 'images' in os.listdir(dr):
            os.mkdir(dr+'/images')
        if not 'video' in os.listdir(dr):
            os.mkdir(dr+'/video')

def ocr_vehicle(filename):
    url = "https://cloud.eyedea.cz/api/v2/cardetect.json"

    payload = {'email': 'rohan27bhandari@outlook.com',
    'password': '1199efa85',
    'Content-type': 'image/jpeg'}
    files = [
    ('upload', open(filename, 'rb'))
    ]
    headers= {}

    response = requests.request("POST", url, headers=headers, data = payload, files = files)
    json_data =  json.loads(response.text.encode('utf8'))
    message = None
    try:
        message = 'License Plate(s) detected: '
        initial_str = message
        for car in json_data['photos'][0]['tags']:
            message += car['lp_text_content'] + ', '
        if message == initial_str:
            return 'Car number plates not detected'
        message = message[:-2]
    except:
        message = 'Car number plates not detected'
    return message


@app.route('/api/postvideo', methods=['POST'])
@cross_origin()
def postVideo():
    global inputfilename
    if request.method != 'POST':
        response = jsonify(success=False)
        return response
    cleanMedia()
    createDirectories()
    inputVideo = request.files['video']
    inputVideo.save(secure_filename(inputVideo.filename))
    # extract one frame and store it
    path = './%s' %(secure_filename(inputVideo.filename))
    inputfilename = secure_filename(inputVideo.filename)
    vidObj = cv2.VideoCapture(path)
    success, image = vidObj.read()
    if success == 1:
        cv2.imwrite("%s_frame.jpg" % secure_filename(inputVideo.filename), image)
    response = jsonify(success=True)
    return response

@app.route('/api/postfeature', methods=['POST'])
@cross_origin()
def postFeature():
    global feature
    if request.method != 'POST':
        response = jsonify(success=False)
        return response
    feature = request.form.get('feature')
    print(val for val in request.args.keys())
    print("Now feature in backend is ", feature)
    response = jsonify(success=True)
    return response

@app.route('/api/getframe/<path:filename>', methods=['GET'])
@cross_origin()
def getFrame(filename):
    if request.method != 'GET':
        response = jsonify(success=False)
        return response
    # return an extracted frame from posted video
    images_path = './'
    imagename = filename + '_frame.jpg'
    print(imagename)
    response = send_from_directory(images_path, imagename, as_attachment=True)
    return response

@app.route('/api/postparameters', methods=['POST'])
@cross_origin()
def postParameters():
    global processingDone, inputfilename
    if request.method != 'POST':
        response = jsonify(success=False)
        return response
    # Post parameters inputted by User
    speedLimit = request.form.get('speedL')
    print("speed", speedLimit)
    laneCoordinates = request.form.get('laneC')
    print("lane", laneCoordinates)
    zebraCoordinates = request.form.get('zebraC')
    print(type(zebraCoordinates))
    print("zebra", zebraCoordinates)
    pedestrianCoordinates = request.form.get('pedestrianC')
    print("pedes", pedestrianCoordinates)
    roadL = request.form.get('roadL')
    print("roadLength", roadL)
    
    metadata = {
        'speed_limit': json.loads(speedLimit),
        'lane_data': json.loads(laneCoordinates),
        'zebra_crossing': json.loads(zebraCoordinates),
        'pedestrian_area': json.loads(pedestrianCoordinates),
        'road_length': json.loads(roadL)
    }
    
    video_frame_convertor = VideoToFrame(inputfilename)
    video_frame_convertor.generate_frames_from_video()
    video_frames, fps = video_frame_convertor.return_frame_data()
    
    composite_rule_object = CompositeRuleObject(metadata, video_frames, fps)
    composite_rule_object.process_rules()
    composite_rule_object.save_videos()
    composite_rule_object.save_snapshots()
    
    # while not processingDone: continue
    response = jsonify(success=True)
    return response
    
@app.route("/api/imageslist/<path:feature>")
@cross_origin()
def listImages(feature):
    """Endpoint to list images on the server.
    """
    files = []
    if feature != 'default':
        images_path = './%s/images/' % (feature)
        if not os.path.isdir(images_path):
            createDirectories()
            response = jsonify(files)
            return response
        for filename in os.listdir(images_path):
            path = os.path.join(images_path, filename)
            if os.path.isfile(path):
                if filename[0] != '.':
                    caption = ocr_vehicle(feature + '/images/' + filename)
                    files.append('/api/getimage?feature={}&filename={}&caption={}'.format(feature,filename, caption))
    else:
        for feature in rule_list:
            images_path = './%s/images/' % (feature)
            if not os.path.isdir(images_path):
                createDirectories()
                continue
            for filename in os.listdir(images_path):
                path = os.path.join(images_path, filename)
                if os.path.isfile(path):
                    if filename[0] != '.':
                        caption = ocr_vehicle(feature + '/images/' + filename) 
                        files.append('/api/getimage?feature={}&filename={}&caption={}'.format(feature,filename, caption))
    response = jsonify(files)
    return response

@app.route("/api/getimage")
@cross_origin()
def getImage():
    """Render an image on frontend"""
    feature = request.args.get('feature')
    filename = request.args.get('filename')
    imagesPath = './%s/images/' % (feature)
    response = send_from_directory(imagesPath, filename, as_attachment=True, cache_timeout=0)
    response.cache_control.max_age = 0
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
    
@app.route('/api/getvideo/<path:feature>')
@cross_origin()
def getVideo(feature):
    feature_path = './%s/video/' % (feature)
    for filename in os.listdir(feature_path):
        path = os.path.join(feature_path, filename)
        if os.path.isfile(path):
            if filename[0] != '.':
                break
    else:
        feature_path = './default/video/'
        for filename in os.listdir(feature_path):
            path = os.path.join(feature_path, filename)
            if os.path.isfile(path):
                if filename[0] != '.':
                    break
    start, end = get_range(request)
    response = partial_response(path, start, end)
    return response

if __name__ == '__main__':
    # Uncomment following line for debugging
    #logging.basicConfig(level=logging.INFO)
    # Optimized server for deployment
    #http_server = HTTPServer(WSGIContainer(app))  
    #http_server.listen(PORT)
    #IOLoop.instance().start()

    # Server for development
    cleanMedia()    # comment this line during development to avoid deletion of media files
    createDirectories()
    http_server = HTTPServer(WSGIContainer(app))  
    http_server.listen(PORT)
    IOLoop.instance().start()
    # app.run(host=HOST, port=PORT, debug=True)
