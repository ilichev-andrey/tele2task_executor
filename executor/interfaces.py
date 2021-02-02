from abc import ABC, ABCMeta, abstractmethod
from typing import Dict


class LoadableFromDict(ABC):
    @abstractmethod
    def load_from_dict(self, data: Dict) -> bool:
        pass


class ConvertibleToDict(ABC):
    @abstractmethod
    def to_dict(self) -> Dict:
        pass


class Serializable(LoadableFromDict, ConvertibleToDict, metaclass=ABCMeta):
    pass
