import unittest

from command_responses.selling_lots import SellingLotsResponse
from containers import Summary
from enums import CommandStatus


class TestSellingLotsResponse(unittest.TestCase):
    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'status': {
                'code': CommandStatus.RECEIVED_SUCCESSFULLY.value,
                'message': CommandStatus.RECEIVED_SUCCESSFULLY.name
            },
            'summary': {
                'gigabytes': 3,
                'minutes': 2,
                'sms': 1
            }
        }

        response = SellingLotsResponse(
            command_id='command_id',
            status=CommandStatus.RECEIVED_SUCCESSFULLY,
            summary=Summary(gigabytes=3, minutes=2, sms=1)
        )
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
