import json

from tele2client.wrappers import LoggerWrap

from command_executors.command_executor import CommandExecutor
from command_responses.selling_lots import SellingLotsResponse
from commands.selling_lots import SellingLotsCommand
from containers import Task
from enums import CommandStatus
from net import Client
from task.task_manager import TaskManager


class SellingLotsExecutor(CommandExecutor):
    _task_manager = TaskManager

    def __init__(self, task_manager: TaskManager):
        self._task_manager = task_manager

    async def execute(self, command: SellingLotsCommand, client: Client) -> bool:
        LoggerWrap().get_logger().info(f'Выполнение команды по добавлению лотов на продажу. {command}')

        summary = await self._task_manager.add_task(Task(
            phone_number=command.phone_number,
            access_token=command.access_token,
            need_to_sell=command.summary
        ))

        response = SellingLotsResponse(
            command_id=command.id,
            status=CommandStatus.RECEIVED_SUCCESSFULLY,
            summary=summary
        )
        await client.writeline(json.dumps(response.to_dict()))

        LoggerWrap().get_logger().info(f'Выполнена команда по добавлению лотов на продажу. {command}')
        return True
