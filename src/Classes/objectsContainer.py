from Classes.temporaryObject import TemporaryObject
from Classes.object import Object


class ObjectsContainer:
    def __init__(self):
        self.objects = []
        self.next_ID = 0

    def add_object(self, tmp_object: TemporaryObject):
        new_obj = Object(self.next_ID, tmp_object)
        self.next_ID += 1
        self.objects.append(new_obj)

    def age_all_objects(self):
        for obj in self.objects:
            obj.increase_age()
            if obj.is_too_old():
                self.delete_object(obj)

    def get_element_by_tmp_obj(self, _tmp_object: TemporaryObject) -> Object:
        found_obj = None
        for obj in self.objects:
            if obj.is_this_me(_tmp_object):
                obj.update_coords(_tmp_object.centre_x, _tmp_object.centre_y,
                                  _tmp_object.bounding_box_coords)
                found_obj = obj
        return found_obj

    def delete_objects_outside_borders(self):
        """Deletes objects, which is out of border"""
        for obj in self.objects:
            if obj.check_border_crossing():
                self.delete_object(obj)

    def delete_object(self, obj):
        self.objects.remove(obj)
        del obj
