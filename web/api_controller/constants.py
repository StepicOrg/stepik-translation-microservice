from enum import Enum, unique


@unique
class RequestedObject(Enum):
    STEP = 'step'
    COURSE = 'course'
    LESSON = 'lesson'
    STEP_SOURCE = 'step-source'
    SERVICE = 'service'
    ATTEMPT = 'attempt'
