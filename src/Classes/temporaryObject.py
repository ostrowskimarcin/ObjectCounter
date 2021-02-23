import cv2

import config


class TemporaryObject:

    def __init__(self, contour):
        self.contour = contour
        self.moment = cv2.moments(contour)
        self.valid = False
        self.bounding_box_coords = []

        self.__calculate_centre_coords()
        self.__calculate_bounding_box_coords(contour)

    def __calculate_centre_coords(self):
        self.centre_x = int(self.moment['m10'] / self.moment['m00'])
        self.centre_y = int(self.moment['m01'] / self.moment['m00'])

    def __calculate_bounding_box_coords(self, _contour):
        box_x, box_y, box_w, box_h = cv2.boundingRect(_contour)
        self.bounding_box_coords = [box_x, box_y, box_w, box_h]

    def is_valid(self) -> bool:
        self.valid = self.__is_size_valid() and self.__is_position_valid()
        return self.valid

    def __is_size_valid(self) -> bool:
        area = cv2.contourArea(self.contour)
        return area > config.OBJECT_SIZE_DETECTION_THRESHOLD

    def __is_position_valid(self) -> bool:
        return config.DETECTION_BORDER_EXIT >= self.centre_y >= config.DETECTION_BORDER_ENTER

    def get_left_top_corner(self):
        return tuple(self.bounding_box_coords[:2])

    def get_right_bottom_corner(self):
        x = self.bounding_box_coords[0] + self.bounding_box_coords[2]
        y = self.bounding_box_coords[1] + self.bounding_box_coords[3]
        return x, y