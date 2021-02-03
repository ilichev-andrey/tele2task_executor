import unittest

from ddt import ddt, idata

from executor.containers import *


def provider_load_from_dict():
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
    @idata(provider_load_from_dict())
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


if __name__ == '__main__':
    unittest.main()
