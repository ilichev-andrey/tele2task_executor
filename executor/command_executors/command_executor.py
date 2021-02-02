from abc import ABC, abstractmethod

from commands.command import Command


class CommandExecutor(ABC):
    @abstractmethod
    def execute(self, command: Command) -> bool:
        pass
