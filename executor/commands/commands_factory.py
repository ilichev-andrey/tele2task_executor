import exceptions
from commands.abort_selling_all_lots import AbortSellingAllLotsCommand
from commands.command import Command
from commands.selling_lots import SellingLotsCommand
from enums import CommandType


def create(command_type: CommandType) -> Command:
    """
    :raises:
        UnknownCommand если команда данного типа не поддерживается
    """

    if command_type == CommandType.ABORT_SELLING_ALL_LOTS:
        return AbortSellingAllLotsCommand()
    if command_type == CommandType.SELLING_LOTS:
        return SellingLotsCommand()

    raise exceptions.UnknownCommand(f'Не поддерживается команда данного типа: {command_type}')
