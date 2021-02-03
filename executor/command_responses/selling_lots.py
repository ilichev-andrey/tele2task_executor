from typing import Dict

from command_responses.command_response import CommandResponse
from containers import Summary
from enums import CommandStatus


class SellingLotsResponse(CommandResponse):
    _summary = Summary

    def __init__(self, command_id: str, status: CommandStatus, summary: Summary):
        super().__init__(command_id, status)
        self._summary = summary

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['summary'] = self._summary.to_dict()
        return data
