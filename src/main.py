import cv2

from Classes.programState import ProgramState, Room
from Classes.temporaryObject import TemporaryObject
from Classes.objectsContainer import ObjectsContainer
from Drive.drive import Drive
from cvOperations import morphological_operations, find_contours
from argumentParser import get_arguments_from_parser

if __name__ == '__main__':
    state = ProgramState()
    objects = ObjectsContainer()
    drive = Drive()
    ProgramState.print_detection_info()

    args = get_arguments_from_parser()
    state.process_arguments(args)

    while state.video_handler.read_new_frame():
        objects.age_all_objects()

        img_bin = morphological_operations(state)
        contours = find_contours(img_bin, state)

        for cnt in contours:
            tmp_object = TemporaryObject(cnt)
            if tmp_object.is_valid():
                state.draw_object(tmp_object)
                obj = objects.get_element_by_tmp_obj(tmp_object)
                if obj is not None:
                    obj.check_lines_crossing(state.room, state.video_handler, drive)
                else:
                    objects.add_object(tmp_object)

        objects.delete_objects_outside_borders()
        state.draw_lines_and_text()

        state.show_frame()

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            state.continue_loop = False
            break

    state.video_handler.release_camera()
    cv2.destroyAllWindows()
