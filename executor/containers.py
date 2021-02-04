from datetime import datetime
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

    def __eq__(self, other: 'Summary'):
        return self.minutes == other.minutes and self.gigabytes == other.gigabytes and self.sms == other.sms

    def __ne__(self, other: 'Summary'):
        return not self.__ne__(other)

    def increment(self, other: 'Summary'):
        self.gigabytes += other.gigabytes
        self.minutes += other.minutes
        self.sms += other.sms

    def decrement(self, other: 'Summary'):
        self.gigabytes -= other.gigabytes
        self.minutes -= other.minutes
        self.sms -= other.sms

    def set(self, other: 'Summary'):
        self.gigabytes = other.gigabytes
        self.minutes = other.minutes
        self.sms = other.sms

    def increment_minutes(self, minutes: int):
        self.minutes += int(minutes)

    def increment_gigabytes(self, gigabytes: int):
        self.gigabytes += int(gigabytes)

    def increment_sms(self, sms: int):
        self.sms += int(sms)

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('gigabytes', 'minutes', 'sms')):
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


class AccessToken(Serializable):
    token: str
    expired_dt: datetime

    def __init__(self):
        self.token = ''
        self.expired_dt = datetime.fromtimestamp(0)

    def __eq__(self, other: 'AccessToken'):
        return self.token == other.token and self.expired_dt == other.expired_dt

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('token', 'expired_dt')):
            return False

        if type(data['expired_dt']) != int:
            return False

        self.token = str(data['token'])
        self.expired_dt = datetime.fromtimestamp(data['expired_dt'])
        return True

    def to_dict(self) -> Dict:
        return {
            'token': self.token,
            'expired_dt': int(datetime.timestamp(self.expired_dt))
        }
