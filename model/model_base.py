from enum import Enum


class ModelStatus(str, Enum):
    
    INITIAL = "initial"
    BUILDING = "building"
    READY = "ready"
    FAILED = "failed"
    INVALID = "invalid"
    DELETED = "deleted"
    UNKNOWN = "unknown"


class Modelbase(object):
    def __init__(self,*args,**krgs):
        self._model_status = ModelStatus.FAILED
    
    @property
    def model_status(self):
        return self._model_status