import asyncio
from typing import List

from tele2client.client import Tele2Client
from tele2client.exceptions import BaseTele2ClientException
from tele2client.wrappers.logger import LoggerWrap

import configs
import containers
from lot.lot_manager import LotManager


class TaskManager(object):
    _config: configs.TaskConfig
    _tasks: List[containers.Task]
    _clients: containers.Clients
    _lot_manager: LotManager

    def __init__(self, config: configs.TaskConfig, lot_manager: LotManager):
        self._config = config
        self._tasks = []
        self._clients = containers.Clients()
        self._lot_manager = lot_manager

    async def add_task(self, task: containers.Task):
        if self._clients.has(task.phone_number):
            # В новой задаче получены новые данные авторизации клиента, поэтому пересоздаем объект Tele2Client
            client = self._clients.get(task.phone_number)
            await client.close()

        self._clients.add(await self.create_new_client(task.phone_number, task.access_token))
        self._tasks.append(task)

    async def run(self):
        while True:
            await asyncio.sleep(self._config.execution_interval_seconds)
            await self._handle_tasks()

    async def _handle_tasks(self):
        LoggerWrap().get_logger().info('handle_tasks')
        for task in self._tasks:
            await self._handle_task(task)

    async def _handle_task(self, task: containers.Task):
        try:
            task.lots = await self._lot_manager.renew(task.lots, task.summary, self._clients.get(task.phone_number))
        except BaseTele2ClientException:
            LoggerWrap().get_logger().warning('Не удалось пересоздать лоты')

    @staticmethod
    async def create_new_client(phone_number: str, access_token: containers.AccessToken) -> Tele2Client:
        client = Tele2Client(phone_number)
        await client.auth_with_params(access_token=access_token)
        return client
