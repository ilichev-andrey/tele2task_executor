from typing import Dict

from commands.command import Command
from enums import CommandType


class AbortSellingAllLotsCommand(Command):
    phone_number = str

    def __init__(self):
        super().__init__()
        self.phone_number = ''

    def get_type(self) -> CommandType:
        return CommandType.ABORT_SELLING_ALL_LOTS

    def load_from_dict(self, data: Dict) -> bool:
        return False
