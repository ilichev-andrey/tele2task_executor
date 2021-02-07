from typing import Dict

from commands.command import Command
from containers import Summary, AccessToken
from enums import CommandType


class SellingLotsCommand(Command):
    phone_number = str
    access_token = AccessToken
    summary = Summary

    def __init__(self, command_id='', phone_number='', access_token=AccessToken(), summary=Summary()):
        super().__init__(command_id=command_id)
        self.phone_number = phone_number
        self.access_token = access_token
        self.summary = summary

    def __str__(self):
        return f'SellingLotsCommand(id={self.id}, phone_number={self.phone_number}, ' \
               f'access_token={str(self.access_token)}, summary={str(self.summary)})'

    def get_type(self) -> CommandType:
        return CommandType.SELLING_LOTS

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('phone_number', 'access_token', 'summary')):
            return False

        access_token = AccessToken()
        if not access_token.load_from_dict(data['access_token']):
            return False

        summary = Summary()
        if not summary.load_from_dict(data['summary']):
            return False

        if not super().load_from_dict(data):
            return False

        self.phone_number = data['phone_number']
        self.access_token = access_token
        self.summary = summary
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['phone_number'] = self.phone_number
        data['access_token'] = self.access_token.to_dict()
        data['summary'] = self.summary.to_dict()
        return data
