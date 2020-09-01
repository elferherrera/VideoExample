import os
import time
import logging
import importlib
import cv2
import imutils

# Modules imported from this project
from utils_config import Config, LOG_FORMAT
from camera.base_camera import BaseCamera

import api

class CameraFile(BaseCamera):
    """Class to detect faces and guns"""

    @staticmethod
    def frames():
        # Initial time to generate a frame
        init_time = time.time()

        # Create stream to video file based on the config file
        # this file will be streamed until the name of the file is changed
        camera_file = os.path.join(
            api.video_folder, 
            Config.get('video.player', 'FILE_NAME'))

        camera = cv2.VideoCapture(camera_file)

        if not camera.isOpened():
            logging.error('Camera not opened')
            api.camera_info['video_event'] = False

        else:
            api.camera_info['video_event'] = True


        while api.camera_info['video_event']:
            # Configured sleep time to try to match the speed at
            # which the video os supposed to be played
            # the value of frames per second comes from the 
            # configuration file
            sleep = 1 / Config.getfloat('video.player', 'FRAMES_PER_SECOND')

            # read current frame
            ret, img = camera.read()

            if ret:

                # if the option is True that means the video was recorded
                # upside down. It is necessary to flip the image before it 
                # is sent to the endpoint
                if Config.getboolean('video.player', 'FLIP_VIDEO'):
                    img = imutils.rotate(img, 180)

                # encode as a jpeg image and return it
                yield cv2.imencode('.jpg', img)[1].tobytes()

                # Storing information in dictionary to be shown in 
                # the info endpoint
                height, width = img.shape[:2]

                api.camera_info['shape'] = {'width': width, 'height': height}
                api.camera_info['file'] = Config.get('video.player', 'FILE_NAME')
                api.camera_info['fps_config'] = Config.getfloat('video.player', 'FRAMES_PER_SECOND')

                # Calculating real sleep time in video stream to 
                # maintain constant video speed
                real_sleep = max(0, sleep - (time.time() - init_time))
                time.sleep(real_sleep)

                api.camera_info['sleep'] = real_sleep
                init_time = time.time()

            else:
                # If there are no more frames to load the video
                # is loaded again and added to the loop
                camera_file = os.path.join(
                    api.video_folder, 
                    Config.get('video.player', 'FILE_NAME'))

                camera = cv2.VideoCapture(camera_file)

