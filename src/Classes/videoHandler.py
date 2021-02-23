import os
import sys
from enum import Enum

import cv2

import config


class VideoHandler:
    def __init__(self):
        self.__video_source = VideoSource.CAMERA
        self.video_handler = None
        self.actual_frame = None
        self.actual_frame_raw = None

    def initialize(self, source: str):
        if os.path.isfile(source):
            self.initialize_video(source)
        elif source.isdigit():
            self.initialize_camera(int(source))
        else:
            print("Bad source parameter specified")
            sys.exit()

    def initialize_camera(self, camera_number=0):
        self.video_handler = cv2.VideoCapture(camera_number)

    def initialize_video(self, path: str):
        self.__video_source = VideoSource.RECORDED_VIDEO
        self.video_handler = cv2.VideoCapture(path)

    def release_camera(self):
        self.video_handler.release()

    def read_new_frame(self) -> bool:
        if self.__video_source == VideoSource.CAMERA:
            self.video_handler.set(3, config.FRAME_WIDTH)
            self.video_handler.set(4, config.FRAME_HEIGHT)
        flag, self.actual_frame = self.video_handler.read()
        if self.__video_source == VideoSource.RECORDED_VIDEO and flag:
            self.actual_frame = cv2.resize(self.actual_frame,
                                           (config.FRAME_WIDTH, config.FRAME_HEIGHT),
                                           interpolation=cv2.INTER_AREA)
        self.actual_frame_raw = self.actual_frame.copy()

        return flag


class VideoSource(Enum):
    CAMERA = 0
    RECORDED_VIDEO = 1

