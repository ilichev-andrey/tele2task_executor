import unittest
from ddt import ddt, idata

from command_responses.summary import SummaryResponse
from containers import Summary
from enums import CommandStatus
from interfaces import LoadableFromDict


class Provider(unittest.TestCase):
    def provider_load_from_dict(self):
        default = SummaryResponse()
        failed_result = {
            'func_result': False,
            'id': default.id,
            'status': default.status,
            'summary': default.summary
        }

        summary_data = {
            'gigabytes': 3,
            'minutes': 2,
            'sms': 1
        }

        def load(obj: LoadableFromDict, data):
            self.assertTrue(obj.load_from_dict(data))
            return obj

        cases = [
            # Нет параметра summary
            {
                'data': {},
                'expected': failed_result
            },
            # Не удалось загрузить данные в Summary
            {
                'data': {'summary': {}},
                'expected': failed_result
            },
            # Не удалось загрузить даные в CommandResponse (отсутствует параметр статус)
            {
                'data': {
                    'summary': summary_data,
                    'id': 'command_id'
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
                    },
                    'summary': summary_data
                },
                'expected': {
                    'func_result': True,
                    'id': 'command_id',
                    'status': CommandStatus.COMPLETED_EXECUTION,
                    'summary': load(Summary(), summary_data)
                }
            }
        ]
        for case in cases:
            yield case


@ddt
class TestSummaryResponse(unittest.TestCase):
    @idata(Provider().provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = SummaryResponse()
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)
        self.assertEqual(expected['status'], response.status)
        self.assertEqual(expected['summary'], response.summary)

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

        response = SummaryResponse()
        response.id = 'command_id'
        response.status = CommandStatus.RECEIVED_SUCCESSFULLY
        response.summary = Summary(gigabytes=3, minutes=2, sms=1)
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
