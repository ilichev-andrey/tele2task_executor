import exceptions
from command_executors.abort_selling_all_lots import AbortSellingAllLotsExecutor
from command_executors.command_executor import CommandExecutor
from command_executors.selling_lots import SellingLotsExecutor
from enums import CommandType
from task.task_manager import TaskManager


def create(command_type: CommandType, task_manager: TaskManager) -> CommandExecutor:
    """
    :raises:
        UnknownCommand если не найден исполнитель для команды данного типа
    """

    if command_type == CommandType.ABORT_SELLING_ALL_LOTS:
        return AbortSellingAllLotsExecutor(task_manager)
    if command_type == CommandType.SELLING_LOTS:
        return SellingLotsExecutor(task_manager)

    raise exceptions.UnknownCommand(f'Не найден исполнитель для команды данного типа: {command_type}')
