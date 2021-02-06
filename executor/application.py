from typing import Dict

from tele2client.wrappers import LoggerWrap

import exceptions
from command_executors import executors_factory
from commands import commands_factory
from commands.command import Command
from configs import Config
from lot.lot_manager import LotManager
from task.task_manager import TaskManager


class Application(object):
    _task_manager = TaskManager
    _lot_manager = LotManager

    def __init__(self, config: Config):
        self._lot_manager = LotManager(config.lot)
        self._task_manager = TaskManager(config.task, self._lot_manager)

    def run(self):
        pass

    def _read_data(self):
        # получить данные
        pass

    def _execute_commands(self):
        data = {}
        try:
            command = self._handle_command(data)
        except exceptions.InvalidFormatCommand as e:
            LoggerWrap().get_logger().exception(str(e))
        else:
            executor = executors_factory.create(command.get_type())
            executor.execute(command)

    @staticmethod
    def _handle_command(data: Dict) -> Command:
        """
        :raises
            InvalidFormatCommand если не удалось загрузить команду
        """

        if 'type' not in data:
            raise exceptions.InvalidFormatCommand(f'Не найден параметр "type" в данных: {data}')

        command = commands_factory.create(data['type'])
        if not command.load_from_dict(data):
            raise exceptions.InvalidFormatCommand(f'Не удалось загрузить команду, данные: {data}')

        return command
