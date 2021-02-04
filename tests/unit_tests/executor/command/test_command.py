import unittest

from ddt import ddt, idata

from commands.command import Command
from enums import CommandType


class CommandForTest(Command):
    def get_type(self) -> CommandType:
        return CommandType.UNKNOWN


def provider_load_from_dict():
    default = CommandForTest()
    failed_result = {
        'func_result': False,
        'id': default.id
    }

    cases = [
        # Нет параметра id
        {
            'data': {},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id'
            },
            'expected': {
                'func_result': True,
                'id': 'command_id'
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

        command = CommandForTest()
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)

    def test_to_dict(self):
        expected = {
            'id': 'command_id'
        }

        command = CommandForTest()
        command.id = 'command_id'
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
