import unittest
from datetime import datetime

from ddt import ddt, idata

from commands.selling_lots import SellingLotsCommand
from containers import AccessToken, Summary
from interfaces import LoadableFromDict


class Provider(unittest.TestCase):
    def provider_load_from_dict(self):
        default = SellingLotsCommand()
        failed_result = {
            'func_result': False,
            'id': default.id,
            'phone_number': default.phone_number,
            'access_token': default.access_token,
            'summary': default.summary
        }

        phone_number = '8800300600'
        access_token_data = {
            'token': 'token',
            'expired_dt': 1
        }

        summary_data = {
            'gigabytes': 1,
            'minutes': 2,
            'sms': 3
        }

        def load(obj: LoadableFromDict, data):
            self.assertTrue(obj.load_from_dict(data))
            return obj

        cases = [
            # Нет параметра phone_number
            {
                'data': {'access_token': access_token_data, 'summary': summary_data},
                'expected': failed_result
            },
            # Нет параметра access_token
            {
                'data': {'phone_number': phone_number, 'summary': summary_data},
                'expected': failed_result
            },
            # Нет параметра summary
            {
                'data': {'phone_number': phone_number, 'access_token': access_token_data},
                'expected': failed_result
            },
            # Не удалось загрузить AccessToken
            {
                'data': {'phone_number': phone_number, 'access_token': {'invalid_data'}, 'summary': summary_data},
                'expected': failed_result
            },
            # Не удалось загрузить Summary
            {
                'data': {'phone_number': phone_number, 'access_token': access_token_data, 'summary': {'invalid_data'}},
                'expected': failed_result
            },
            # Не удалось загрузить Command (нет параметра id)
            {
                'data': {'phone_number': phone_number, 'access_token': access_token_data, 'summary': summary_data},
                'expected': failed_result
            },
            # Успешная загрузка данных
            {
                'data': {
                    'id': 'command_id',
                    'phone_number': phone_number,
                    'access_token': access_token_data,
                    'summary': summary_data
                },
                'expected': {
                    'func_result': True,
                    'id': 'command_id',
                    'phone_number': phone_number,
                    'access_token': load(AccessToken(), access_token_data),
                    'summary': load(Summary(), summary_data)
                }
            }
        ]
        for case in cases:
            yield case


@ddt
class TestSellingLotsCommand(unittest.TestCase):
    @idata(Provider().provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        command = SellingLotsCommand()
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['access_token'], command.access_token)
        self.assertEqual(expected['summary'], command.summary)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'phone_number': '88003000600',
            'access_token': {
                'token': 'token',
                'expired_dt': 1
            },
            'summary': {
                'gigabytes': 1,
                'minutes': 2,
                'sms': 3
            }
        }

        command = SellingLotsCommand()
        command.id = 'command_id'
        command.phone_number = '88003000600'
        command.access_token.token = 'token'
        command.access_token.expired_dt = datetime.fromtimestamp(1)
        command.summary = Summary(gigabytes=1, minutes=2, sms=3)
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
