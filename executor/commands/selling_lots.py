from typing import Dict

from tele2client.containers import AccessToken

from commands.command import Command
from containers import Summary
from enums import CommandType


class SellingLotsCommand(Command):
    access_token = AccessToken
    summary = Summary

    def __init__(self):
        super().__init__()
        self.access_token = AccessToken()
        self.summary = Summary()

    def get_type(self) -> CommandType:
        return CommandType.SELLING_LOTS

    def load_from_dict(self, data: Dict) -> bool:
        return False
