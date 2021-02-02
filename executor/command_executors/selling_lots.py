from command_executors.command_executor import CommandExecutor
from commands.command import Command


class SellingLotsExecutor(CommandExecutor):
    def execute(self, command: Command) -> bool:
        return False
