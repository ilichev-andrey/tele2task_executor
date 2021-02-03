from typing import Dict

from interfaces import Serializable


class Summary(Serializable):
    gigabytes: int
    minutes: int
    sms: int

    def __init__(self, gigabytes: int = 0, minutes: int = 0, sms: int = 0):
        self.gigabytes = int(gigabytes)
        self.minutes = int(minutes)
        self.sms = int(sms)

    def __repr__(self):
        return f'{self.__class__.__name__}(gigabytes={self.gigabytes}, minutes={self.minutes}, sms={self.sms})'

    def __ne__(self, summary: 'Summary'):
        return self.minutes != summary.minutes and self.gigabytes != summary.gigabytes and self.sms != summary.sms

    def increment(self, summary: 'Summary'):
        self.gigabytes += summary.gigabytes
        self.minutes += summary.minutes
        self.sms += summary.sms

    def decrement(self, summary: 'Summary'):
        self.gigabytes -= summary.gigabytes
        self.minutes -= summary.minutes
        self.sms -= summary.sms

    def set(self, summary: 'Summary'):
        self.gigabytes = summary.gigabytes
        self.minutes = summary.minutes
        self.sms = summary.sms

    def increment_minutes(self, minutes: int):
        self.minutes += int(minutes)

    def increment_gigabytes(self, gigabytes: int):
        self.gigabytes += int(gigabytes)

    def increment_sms(self, sms: int):
        self.sms += int(sms)

    def load_from_dict(self, data: Dict) -> bool:
        keys = {'gigabytes', 'minutes', 'sms'}
        if not keys.issubset(data.keys()):
            return False

        self.gigabytes = int(data['gigabytes'])
        self.minutes = int(data['minutes'])
        self.sms = int(data['sms'])
        return True

    def to_dict(self) -> Dict:
        return {
            'gigabytes': self.gigabytes,
            'minutes': self.minutes,
            'sms': self.sms
        }
