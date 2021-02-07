import asyncio

from tele2client.client import Tele2Client
from tele2client.exceptions import BaseTele2ClientException
from tele2client.wrappers.logger import LoggerWrap

import configs
import containers
from lot.lot_manager import LotManager


class TaskManager(object):
    _config: configs.TaskConfig
    _tasks: containers.Tasks
    _clients: containers.Clients
    _lot_manager: LotManager

    def __init__(self, config: configs.TaskConfig, lot_manager: LotManager):
        self._config = config
        self._tasks = containers.Tasks()
        self._clients = containers.Clients()
        self._lot_manager = lot_manager
        self._lock = asyncio.Lock()

    async def add_task(self, task: containers.Task) -> containers.Summary:
        phone_number = task.phone_number
        if self._clients.has(phone_number):
            # В новой задаче получены новые данные авторизации клиента, поэтому пересоздаем объект Tele2Client
            client = self._clients.get(phone_number)
            await client.close()

        if self._tasks.has(phone_number):
            task = self._merge_tasks(self._tasks.get(phone_number), task)

        client = await self._create_tele2client(phone_number, task.access_token)
        async with self._lock:
            self._clients.add(client)
            self._tasks.add(task)
            return await self._lot_manager.get_lots_for_sale(task.need_to_sell, client)

    async def abort_task(self, phone_number: str):
        async with self._lock:
            if self._clients.has(phone_number):
                client = self._clients.get(phone_number)
                await client.close()
                self._clients.remove(phone_number)

            self._tasks.remove(phone_number)

    async def run(self):
        while True:
            await asyncio.sleep(self._config.execution_interval_seconds)
            await self._handle_tasks()

    @staticmethod
    def _merge_tasks(old_task: containers.Task, new_task: containers.Task) -> containers.Task:
        return old_task.merge(new_task)

    async def _handle_tasks(self):
        LoggerWrap().get_logger().info('handle_tasks')
        async with self._lock:
            for task in self._tasks.get_all():
                await self._handle_task(task)

    async def _handle_task(self, task: containers.Task):
        client = self._clients.get(task.phone_number)
        try:
            task.active_lots = await self._lot_manager.renew(task.active_lots, task.need_to_sell, client)
        except BaseTele2ClientException:
            LoggerWrap().get_logger().warning('Не удалось пересоздать лоты')

    @staticmethod
    async def _create_tele2client(phone_number: str, access_token: containers.AccessToken) -> Tele2Client:
        client = Tele2Client(phone_number)
        await client.auth_with_params(access_token=access_token)
        return client
