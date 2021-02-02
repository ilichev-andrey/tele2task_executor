from typing import Dict

from command_executors import executors_factory
from commands import commands_factory
from commands.command import Command


class Application(object):
    _config = Dict

    def __init__(self, config: Dict):
        self._config = config

    def run(self):
        # получить данные
        data = {}

        command = self._handle_command(data)
        executor = executors_factory.create(command.get_type())
        executor.execute(command)

    @staticmethod
    def _handle_command(data: Dict) -> Command:
        """
        :raises
        """

        if 'type' not in data:
            # log
            pass

        command = commands_factory.create(data['type'])
        if not command.load_from_dict(data):
            # log
            pass

        return command
