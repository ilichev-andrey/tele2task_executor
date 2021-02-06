from typing import Dict

from commands.command import Command
from enums import CommandType


class AbortSellingAllLotsCommand(Command):
    phone_number = str

    def __init__(self):
        super().__init__()
        self.phone_number = ''

    def __str__(self):
        return f'AbortSellingAllLotsCommand(id={self.id}, phone_number={self.phone_number})'

    def get_type(self) -> CommandType:
        return CommandType.ABORT_SELLING_ALL_LOTS

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('phone_number',)):
            return False

        if not super().load_from_dict(data):
            return False

        self.phone_number = str(data['phone_number'])
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['phone_number'] = self.phone_number
        return data
