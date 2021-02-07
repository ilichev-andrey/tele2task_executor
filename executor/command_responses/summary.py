from typing import Dict

from command_responses.command_response import CommandResponse
from containers import Summary
from enums import CommandStatus


class SummaryResponse(CommandResponse):
    summary = Summary

    def __init__(self, command_id='', status=CommandStatus.UNKNOWN, summary=Summary()):
        super().__init__(command_id=command_id, status=status)
        self.summary = summary

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('summary',)):
            return False

        summary = Summary()
        if not summary.load_from_dict(data['summary']):
            return False

        if not super().load_from_dict(data):
            return False

        self.summary = summary
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['summary'] = self.summary.to_dict()
        return data
