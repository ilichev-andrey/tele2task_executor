from typing import Dict

from enums import CommandStatus
from interfaces import ConvertibleToDict


class CommandResponse(ConvertibleToDict):
    _id = str
    _status: CommandStatus

    def __init__(self, command_id: str, status: CommandStatus):
        self._id = command_id
        self._status = status

    def to_dict(self) -> Dict:
        return {
            'id': self._id,
            'status': {
                'code': self._status.value,
                'message': self._status.name
            }
        }
