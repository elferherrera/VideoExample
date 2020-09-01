import os
import time
import logging
import importlib
from flask import Flask, Response, jsonify, request

from utils_config import Config

# Modules from this package
import camera
import api

app = Flask(__name__)

# Video folder where all the video files are stored
# This directory will be linked to a docker mount volume
video_folder = Config.get("video.player", "VIDEO_FOLDER")

# Dictionary to store process variables calculated 
# during the video streaming
# The dictionary is sent to client via info endpoint
camera_info = {
    "time_per_100_frames": 0,
    "video_event": True,
    "videos": os.listdir(video_folder)
}


def gen(camera):
    """Video streaming generator function."""
    reference = 100
    counter = 0
    init_time = time.time()

    while True:

        # Getting frame from camera object
        frame = camera.get_frame()

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""

    return Response(
        gen(camera.CameraFile()), 
        mimetype='multipart/x-mixed-replace; boundary=frame')
