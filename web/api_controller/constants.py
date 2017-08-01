from enum import Enum, unique


@unique
class RequestedObject(Enum):
    STEP = 'step'
    COURSE = 'course'
    LESSON = 'lesson'
    CHOICE = 'choice'
    SERVICE = 'service'
