import unittest

from ddt import ddt, idata

from command_responses.command_response import CommandResponse
from enums import CommandStatus


def provider_load_from_dict():
    default = CommandResponse()
    failed_result = {
        'func_result': False,
        'id': default.id,
        'status': default.status
    }

    cases = [
        # Нет параметра id
        {
            'data': {'status': {}},
            'expected': failed_result
        },
        # Нет параметра status
        {
            'data': {'id': 'command_id'},
            'expected': failed_result
        },
        # Нет параметра code
        {
            'data': {
                'id': 'command_id',
                'status': {
                    'message': CommandStatus.COMPLETED_EXECUTION.name
                }
            },
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'status': {
                    'code': CommandStatus.COMPLETED_EXECUTION.value,
                    'message': CommandStatus.COMPLETED_EXECUTION.name
                }
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'status': CommandStatus.COMPLETED_EXECUTION
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = CommandResponse()
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)
        self.assertEqual(expected['status'], response.status)

    def test_to_dict(self):
        status = CommandStatus.COMPLETED_EXECUTION
        expected = {
            'id': 'command_id',
            'status': {
                'code': status.value,
                'message': status.name
            }
        }

        response = CommandResponse()
        response.id = 'command_id'
        response.status = status
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
