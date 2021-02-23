import matplotlib
# matplotlib.use('TkAgg')

import argparse
import numpy as np
import cv2

import matplotlib.pyplot as plt
from pushbullet import Pushbullet

import config
from Classes.videoHandler import VideoHandler


class ProgramState:
    def __init__(self):
        self.continue_loop = True
        self.fgbg_extractor = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.open_kernel = np.ones(config.OPEN_KERNEL_SIZE, np.uint8)
        self.close_kernel = np.ones(config.CLOSE_KERNEL_SIZE, np.uint8)
        self.debug_mode = False
        self.exit_line = ProgramState.__create_line_coords(config.EXIT_LINE_HEIGHT)
        self.entrance_line = ProgramState.__create_line_coords(config.ENTRANCE_LINE_HEIGHT)
        self.top_border_line = ProgramState.__create_line_coords(config.DETECTION_BORDER_ENTER)
        self.bottom_border_line = ProgramState.__create_line_coords(config.DETECTION_BORDER_EXIT)

        # create objects
        self.room = Room()
        self.video_handler = VideoHandler()
        self.debug_frames = None  # not always created object

    def process_arguments(self, args: argparse.Namespace):
        if args.source:
            self.video_handler.initialize(args.source)
        else:
            # default if nothing specified
            self.video_handler.initialize_camera()

        if args.debug:
            self.debug_mode = True
            self.debug_frames = DebugHandler()

        if args.notifications:
            config.NOTIFICATIONS = True

        if args.photos:
            config.SEND_PHOTOS_TO_DRIVE = True

        if args.limit:
            if int(args.limit) > 0:
                config.LIMIT = int(args.limit)

    def show_frame(self):
        cv2.imshow('Object_Counting', self.video_handler.actual_frame)
        if self.debug_mode:
            self.debug_frames.show_debug_frames()

    @staticmethod
    def __create_line_coords(_height: int) -> np.array:
        start_point = [0, _height]
        end_point = [config.FRAME_WIDTH, _height]
        np_line = np.array([start_point, end_point], np.int32).reshape(-1, 1, 2)
        return np_line

    def get_fgbg_mask(self):
        if config.GRAYSCALE:
            img_gray = cv2.cvtColor(self.video_handler.actual_frame, cv2.COLOR_BGR2GRAY)
            if self.debug_mode:
                self.debug_frames.grayscale_frame = img_gray
            return self.fgbg_extractor.apply(img_gray)

        return self.fgbg_extractor.apply(self.video_handler.actual_frame)

    @staticmethod
    def print_detection_info():
        # prog wykrycia obiektu tzn. czy ma pole powierzchni większe
        print('Prog: ', config.OBJECT_SIZE_DETECTION_THRESHOLD)
        print("Czerwona linia WYJSC:", str(config.EXIT_LINE_HEIGHT))
        print("Niebieska linia WEJSC:", str(config.ENTRANCE_LINE_HEIGHT))

    def print_final_information(self):
        print('EOF')
        print('WEJSCIE:', self.room.entrance_cnt)
        print('WYJSCIE:', self.room.exit_cnt)
        self.continue_loop = False

    def draw_lines_and_text(self):
        str_up = 'WEJSCIE: ' + str(self.room.entrance_cnt)
        str_down = 'WYJSCIE: ' + str(self.room.exit_cnt)
        self.video_handler.actual_frame = cv2.polylines(self.video_handler.actual_frame,
                                                        [self.entrance_line], False,
                                                        config.ENTRANCE_LINE_COLOUR,
                                                        thickness=2)
        self.video_handler.actual_frame = cv2.polylines(self.video_handler.actual_frame,
                                                        [self.exit_line],
                                                        False, config.EXIT_LINE_COLOUR,
                                                        thickness=2)
        self.video_handler.actual_frame = cv2.polylines(self.video_handler.actual_frame,
                                                        [self.top_border_line], False,
                                                        (255, 255, 255),
                                                        thickness=1)
        self.video_handler.actual_frame = cv2.polylines(self.video_handler.actual_frame,
                                                        [self.bottom_border_line], False,
                                                        (255, 255, 255),
                                                        thickness=1)
        cv2.putText(self.video_handler.actual_frame, str_up, (10, 40), self.font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(self.video_handler.actual_frame, str_up, (10, 40), self.font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(self.video_handler.actual_frame, str_down, (10, 90), self.font, 0.5, (255, 255, 255), 2,
                    cv2.LINE_AA)
        cv2.putText(self.video_handler.actual_frame, str_down, (10, 90), self.font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    def draw_object(self, _tmp_object):
        self.video_handler.actual_frame = cv2.circle(self.video_handler.actual_frame,
                                                     (_tmp_object.centre_x, _tmp_object.centre_y),
                                                     radius=5,
                                                     color=config.OBJECT_CIRCLE_COLOUR,
                                                     thickness=-1)
        self.video_handler.actual_frame = cv2.rectangle(self.video_handler.actual_frame,
                                                        _tmp_object.get_left_top_corner(),
                                                        _tmp_object.get_right_bottom_corner(),
                                                        config.OBJECT_RECTANGLE_COLOUR,
                                                        thickness=2)

    def draw_object_drive(self, _tmp_object):
        self.video_handler.actual_frame_raw = cv2.circle(self.video_handler.actual_frame,
                                                         (_tmp_object.centre_x, _tmp_object.centre_y),
                                                         radius=5,
                                                         color=config.OBJECT_CIRCLE_COLOUR,
                                                         thickness=-1)
        self.video_handler.actual_frame_raw = cv2.rectangle(self.video_handler.actual_frame,
                                                            _tmp_object.get_left_top_corner(),
                                                            _tmp_object.get_right_bottom_corner(),
                                                            config.OBJECT_RECTANGLE_COLOUR,
                                                            thickness=2)


class DebugHandler:

    def __init__(self):
        self.grayscale_frame = None
        self.foreground_frame = None
        self.blur_frame = None
        self.binary_frame = None

    def show_debug_frames(self):
        _window_offset = 0
        for name, frame in self.__dict__.items():
            cv2.imshow(name, frame)
            _window_offset += config.DEBUG_WINDOW_OFFSET
            cv2.moveWindow(name, _window_offset, 0)


class Room:

    def __init__(self, entrance_cnt=0, exit_cnt=0):
        self.pb = Pushbullet(config.PUSH_KEY)
        self.entrance_cnt = entrance_cnt
        self.exit_cnt = exit_cnt
        self.objects_inside = 0
        self.overpopulation_notification_send = False
        self.underpopulation_notification_send = False

    def proceed_population_notifications(self):
        self.objects_inside = self.get_objects_inside_cnt()

        if self.objects_inside > config.LIMIT and not self.overpopulation_notification_send:
            print("Room overpopulated")
            self.send_overpopulation_push()
            self.overpopulation_notification_send = True
            self.underpopulation_notification_send = False
        elif self.objects_inside <= config.LIMIT and not self.underpopulation_notification_send:
            print("Room is not overpopulated")
            self.send_underpopulation_push()
            self.overpopulation_notification_send = False
            self.underpopulation_notification_send = True

    def get_objects_inside_cnt(self):
        return self.entrance_cnt - self.exit_cnt

    def send_overpopulation_push(self):
        title = "Ostrzeżenie"
        message = "Limit miejsc: " + str(config.LIMIT) + " wyczerpany."
        self.send_push(title, message)

    def send_underpopulation_push(self):
        title = "Powiadomienie"
        message = "Ilość osób w pomieszczeniu mieści się w limicie: " + str(config.LIMIT)
        self.send_push(title, message)

    def send_push(self, title: str, message: str):
        self.pb.push_note(title, message)
