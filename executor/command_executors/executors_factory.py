from command_executors.abort_selling_all_lots import AbortSellingAllLotsExecutor
from command_executors.command_executor import CommandExecutor
from command_executors.selling_lots import SellingLotsExecutor
from enums import CommandType


def create(command_type: CommandType) -> CommandExecutor:
    """
    :raises:

    """

    if command_type == CommandType.ABORT_SELLING_ALL_LOTS:
        return AbortSellingAllLotsExecutor()
    if command_type == CommandType.SELLING_LOTS:
        return SellingLotsExecutor()

    # raise
