from abc import abstractmethod
from typing import Dict

from enums import CommandType
from interfaces import Serializable


class Command(Serializable):
    id = str

    def __init__(self):
        self.id = ''

    @abstractmethod
    def get_type(self) -> CommandType:
        pass

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('id',)):
            return False

        self.id = str(data['id'])
        return True

    def to_dict(self) -> Dict:
        return {'id': self.id}
