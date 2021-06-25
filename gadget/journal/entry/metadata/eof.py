from ..constants import *
from .abstract import Metadata


class EOF(Metadata):
    def __init__(self):
        super().__init__(None, None, EOF_NAME)

    def is_left(self):
        return False

    def is_right(self):
        return False

    def jsonify(self):
        d = dict()
        d[METADATA] = EOF_NAME
        return d

    @staticmethod
    def is_superclass(json_dict: dict):
        return METADATA in json_dict and json_dict[METADATA] == EOF_NAME

    @classmethod
    def cons(cls, json_dict: dict):
        return cls()
