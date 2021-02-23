from random import randint
from enum import Enum
import time
import threading

import cv2

import config
from Classes.temporaryObject import TemporaryObject
from Drive.drive import Drive, Lines


class Object:

    def __init__(self, ID: int, tmp_object: TemporaryObject):
        self.ID = ID
        self.x = tmp_object.centre_x
        self.y = tmp_object.centre_y
        self.bounding_box_coords = tmp_object.bounding_box_coords
        self.max_age = config.MAX_OBJECT_AGE
        self.object_track = []
        self.R = randint(0, 255)
        self.G = randint(0, 255)
        self.B = randint(0, 255)
        self.too_old = False
        self.state = ObjectState.DETECTED
        self.age = 0
        self.dir = None

    def check_lines_crossing(self, _room, _video_handler, _drive: Drive):
        actual_time = time.strftime("%c")
        if self.entrance_line_passed():
            _room.entrance_cnt += 1
            print("ID:", self.ID, 'enter the room at: ', actual_time)
            if config.SEND_PHOTOS_TO_DRIVE:
                self.draw_object_on_frame(_video_handler.actual_frame_raw)
                upload = threading.Thread(target=_drive.upload,
                                          args=(_video_handler.actual_frame_raw, actual_time, self.ID, Lines.ENTRANCE_LINE))
                upload.start()

        elif self.exit_line_passed():
            _room.exit_cnt += 1
            print("ID:", self.ID, 'exit the room at: ', actual_time)
            if config.SEND_PHOTOS_TO_DRIVE:
                self.draw_object_on_frame(_video_handler.actual_frame_raw)
                upload = threading.Thread(target=_drive.upload,
                                          args=(_video_handler.actual_frame_raw, actual_time, self.ID, Lines.EXIT_LINE))
                upload.start()

        if config.NOTIFICATIONS:
            _room.proceed_population_notifications()

    def entrance_line_passed(self):
        if len(self.object_track) >= 2:
            if self.state == ObjectState.DETECTED:
                if self.object_track[-1][1] < config.ENTRANCE_LINE_HEIGHT <= self.object_track[-2][1]:
                    self.state = ObjectState.LINE_PASSED
                    self.dir = 'up'
                    return True
            else:
                return False
        else:
            return False

    def exit_line_passed(self):
        if len(self.object_track) >= 2:
            if self.state == ObjectState.DETECTED:
                if self.object_track[-1][1] > config.EXIT_LINE_HEIGHT >= self.object_track[-2][1]:
                    self.state = ObjectState.LINE_PASSED
                    self.dir = 'down'
                    return True
            else:
                return False
        else:
            return False

    def check_border_crossing(self):
        if self.dir == 'down' and self.y > config.DETECTION_BORDER_EXIT:
            return True
        elif self.dir == 'up' and self.y < config.DETECTION_BORDER_ENTER:
            return True
        else:
            return False

    def update_coords(self, _x, _y, _bounding_box: list):
        self.age = 0
        self.object_track.append([self.x, self.y])
        self.x = _x
        self.y = _y
        self.bounding_box_coords = _bounding_box

    def increase_age(self):
        self.age += 1
        if self.age > self.max_age:
            self.too_old = True
        return True

    def is_this_me(self, _tmp_object: TemporaryObject) -> bool:
        box_w = _tmp_object.bounding_box_coords[2]
        box_h = _tmp_object.bounding_box_coords[3]
        is_width_ok = abs(_tmp_object.centre_x - self.x) <= box_w
        is_height_ok = abs(_tmp_object.centre_y - self.y) <= box_h
        return is_width_ok and is_height_ok

    def get_RGB(self) -> tuple:
        return self.R, self.G, self.B

    def set_too_old(self):
        self.too_old = True

    def is_too_old(self) -> bool:
        return self.age > self.max_age

    def reset_age_cnt(self):
        self.age = 0

    def draw_object_on_frame(self, _cv2_frame):
        _cv2_frame = cv2.circle(_cv2_frame,
                                (self.x, self.y),
                                radius=5,
                                color=config.OBJECT_CIRCLE_COLOUR,
                                thickness=-1)

        _cv2_frame = cv2.rectangle(_cv2_frame,
                                   self.get_left_top_corner(),
                                   self.get_right_bottom_corner(),
                                   config.OBJECT_RECTANGLE_COLOUR,
                                   thickness=2)

    def get_left_top_corner(self):
        return tuple(self.bounding_box_coords[:2])

    def get_right_bottom_corner(self):
        x = self.bounding_box_coords[0] + self.bounding_box_coords[2]
        y = self.bounding_box_coords[1] + self.bounding_box_coords[3]
        return x, y


class ObjectState(Enum):
    DETECTED = 0
    LINE_PASSED = 1
    BORDER_PASSED = 2
