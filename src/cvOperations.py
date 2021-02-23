import cv2

import config
from Classes.programState import ProgramState


def morphological_operations(_state: ProgramState):
    fgbg_mask = _state.get_fgbg_mask()
    blur = cv2.GaussianBlur(fgbg_mask, (5, 5), 0)
    ret, img_bin = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, _state.open_kernel)
    img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, _state.close_kernel)
    if _state.debug_mode:
        _state.debug_frames.foreground_frame = fgbg_mask
        _state.debug_frames.blur_frame = blur
        _state.debug_frames.binary_frame = img_bin
    return img_bin


def find_contours(_img_bin, _state: ProgramState):
    """
    """
    if cv2.__version__ == '4.4.0':
        contours, hierarchy = cv2.findContours(_img_bin,
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
    else:
        image, contours, hierarchy = cv2.findContours(_img_bin,
                                                      cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_SIMPLE)

    return contours
