import asyncio
import json
from typing import Dict

from tele2client.wrappers import LoggerWrap

import exceptions
import net
from command_executors import executors_factory
from commands import commands_factory
from commands.command import Command
from configs import Config
from enums import CommandType
from lot.lot_manager import LotManager
from net import Client
from task.task_manager import TaskManager


class Application(object):
    _config = Config
    _task_manager = TaskManager
    _lot_manager = LotManager

    def __init__(self, config: Config):
        self._config = config
        self._lot_manager = LotManager(config.lot)
        self._task_manager = TaskManager(config.task, self._lot_manager)

    async def run(self):
        await asyncio.gather(
            asyncio.ensure_future(self._run_server()),
            asyncio.ensure_future(self._task_manager.run())
        )

    async def _run_server(self):
        server_config = self._config.server
        server = await net.start_server(handler=self._handle_data, host=server_config.host, port=server_config.port)
        await server.run()

    async def _handle_data(self, client: Client):
        data = await self._read_data(client)
        await self._execute_command(data, client)

    @staticmethod
    async def _read_data(client: Client) -> Dict:
        """
        :raises
            JSONDecodeError если полученная команда не в формате JSON
        """
        data = await client.readline()
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            LoggerWrap().get_logger().exception(str(e))
            raise

    async def _execute_command(self, command_data: Dict, client: Client):
        try:
            command = self._handle_command(command_data)
            executor = executors_factory.create(command.get_type(), self._task_manager)
        except exceptions.CommandException as e:
            LoggerWrap().get_logger().exception(str(e))
        else:
            await executor.execute(command, client)

    @staticmethod
    def _handle_command(data: Dict) -> Command:
        """
        :raises
            UnknownCommand если получена неизвестная команда
            InvalidFormatCommand если не удалось загрузить команду
        """

        if 'type' not in data:
            raise exceptions.InvalidFormatCommand(f'Не найден параметр "type" в данных: {data}')

        command = commands_factory.create(CommandType(data['type']))
        if not command.load_from_dict(data):
            raise exceptions.InvalidFormatCommand(f'Не удалось загрузить команду, данные: {data}')

        LoggerWrap().get_logger().info(f'Команда обработана: {command}')
        return command
