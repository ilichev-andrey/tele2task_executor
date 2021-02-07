import json

from tele2client.wrappers import LoggerWrap

from command_executors.command_executor import CommandExecutor
from command_responses.abort_selling_all_lots import AbortSellingAllLotsResponse
from commands.abort_selling_all_lots import AbortSellingAllLotsCommand
from enums import CommandStatus
from net import Client
from task.task_manager import TaskManager


class AbortSellingAllLotsExecutor(CommandExecutor):
    _task_manager = TaskManager

    def __init__(self, task_manager: TaskManager):
        self._task_manager = task_manager

    async def execute(self, command: AbortSellingAllLotsCommand, client: Client) -> bool:
        LoggerWrap().get_logger().info(f'Выполнение команды прерывания продажи лотов. {command}')

        await self._task_manager.abort_task(command.phone_number)
        await client.writeline(json.dumps(
            AbortSellingAllLotsResponse(command_id=command.id, status=CommandStatus.COMPLETED_EXECUTION).to_dict()
        ))

        LoggerWrap().get_logger().info(f'Выполненена команда прерывания продажи лотов. {command}')
        return True
