import unittest

from ddt import ddt, idata

from commands.abort_selling_all_lots import AbortSellingAllLotsCommand


def provider_load_from_dict():
    default = AbortSellingAllLotsCommand()
    failed_result = {
        'func_result': False,
        'id': default.id,
        'phone_number': default.phone_number
    }

    cases = [
        # Нет параметра phone_number
        {
            'data': {'id': 'command_id'},
            'expected': failed_result
        },
        # Нет параметра id
        {
            'data': {'phone_number': '88003000600'},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'phone_number': '88003000600'
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'phone_number': '88003000600'
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

        command = AbortSellingAllLotsCommand()
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['phone_number'], command.phone_number)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'phone_number': '88003000600'
        }

        command = AbortSellingAllLotsCommand()
        command.id = 'command_id'
        command.phone_number = '88003000600'
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
