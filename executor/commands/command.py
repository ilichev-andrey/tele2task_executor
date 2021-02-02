from abc import ABC, abstractmethod
from typing import Dict

from enums import CommandType
from interfaces import LoadableFromDict


class Command(LoadableFromDict, ABC):
    id = str

    def __init__(self):
        self.id = ''

    @abstractmethod
    def get_type(self) -> CommandType:
        pass

    def load_from_dict(self, data: Dict) -> bool:
        pass
