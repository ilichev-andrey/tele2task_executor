from command_executors.command_executor import CommandExecutor
from commands.command import Command
from lot.lot_manager import LotManager
from task.task_manager import TaskManager


class SellingLotsExecutor(CommandExecutor):
    _task_manager = TaskManager
    _lot_manager = LotManager

    def __init__(self, task_manager: TaskManager, lot_manager: LotManager):
        self._task_manager = task_manager
        self._lot_manager = lot_manager

    def execute(self, command: Command) -> bool:
        return False
