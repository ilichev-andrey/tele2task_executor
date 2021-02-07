from tele2client.wrappers import LoggerWrap

from command_executors.command_executor import CommandExecutor
from commands.selling_lots import SellingLotsCommand
from net import Client
from task.task_manager import TaskManager


class SellingLotsExecutor(CommandExecutor):
    _task_manager = TaskManager

    def __init__(self, task_manager: TaskManager):
        self._task_manager = task_manager

    async def execute(self, command: SellingLotsCommand, client: Client) -> bool:
        LoggerWrap().get_logger().info(f'Выполнение команды по продаже лотов. {command}')
        LoggerWrap().get_logger().info(f'Не удалось выполненить команду по продаже лотов. {command}')
        return False
