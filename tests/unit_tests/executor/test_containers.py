import unittest
from datetime import datetime

from ddt import ddt, idata

from containers import AccessToken, Summary


def summary_provider_load_from_dict():
    default = Summary()
    failed_result = {
        'func_result': False,
        'gigabytes': default.gigabytes,
        'minutes': default.minutes,
        'sms': default.sms
    }

    cases = [
        # Нет параметра gigabytes
        {
            'data': {'minutes': 1, 'sms': 1},
            'expected': failed_result
        },
        # Нет параметра minutes
        {
            'data': {'gigabytes': 1, 'sms': 1},
            'expected': failed_result
        },
        # Нет параметра sms
        {
            'data': {'gigabytes': 1, 'minutes': 1},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {'gigabytes': 1, 'minutes': 2, 'sms': 3},
            'expected': {
                'func_result': True,
                'gigabytes': 1,
                'minutes': 2,
                'sms': 3
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestSummary(unittest.TestCase):
    @idata(summary_provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        summary = Summary()
        self.assertEqual(expected['func_result'], summary.load_from_dict(data))
        self.assertEqual(expected['gigabytes'], summary.gigabytes)
        self.assertEqual(expected['minutes'], summary.minutes)
        self.assertEqual(expected['sms'], summary.sms)

    def test_to_dict(self):
        expected = {
            'gigabytes': 3,
            'minutes': 2,
            'sms': 1
        }

        summary = Summary(gigabytes=3, minutes=2, sms=1)
        self.assertEqual(expected, summary.to_dict())


def token_provider_load_from_dict():
    default = AccessToken()
    failed_result = {
        'func_result': False,
        'token': default.token,
        'expired_dt': default.expired_dt
    }

    timestamp = 1612442967
    cases = [
        # Нет параметра token
        {
            'data': {'expired_dt': 1},
            'expected': failed_result
        },
        # Нет параметра expired_dt
        {
            'data': {'token': 'token'},
            'expected': failed_result
        },
        # Параметр expired_dt не является int
        {
            'data': {'token': 'token', 'expired_dt': '1'},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {'token': 'token', 'expired_dt': timestamp},
            'expected': {
                'func_result': True,
                'token': 'token',
                'expired_dt': datetime.fromtimestamp(timestamp)
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestAccessToken(unittest.TestCase):
    @idata(token_provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        access_token = AccessToken()
        self.assertEqual(expected['func_result'], access_token.load_from_dict(data))
        self.assertEqual(expected['token'], access_token.token)
        self.assertEqual(expected['expired_dt'], access_token.expired_dt)

    def test_to_dict(self):
        timestamp = 1612442967
        expected = {
            'token': 'token',
            'expired_dt': timestamp
        }

        access_token = AccessToken()
        access_token.token = 'token'
        access_token.expired_dt = datetime.fromtimestamp(timestamp)
        self.assertEqual(expected, access_token.to_dict())


if __name__ == '__main__':
    unittest.main()
