from enum import Enum


class CommandType(Enum):
    SELLING_LOTS = 0
    ABORT_SELLING_ALL_LOTS = 1


class CommandStatus(Enum):
    RECEIVED_SUCCESSFULLY = 0
    SOLD_RESTS_CHANGED = 20
    COMPLETED_EXECUTION = 40
    INTERNAL_ERROR = 60
