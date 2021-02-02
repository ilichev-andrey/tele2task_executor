
class Summary(object):
    gigabytes: int
    minutes: int
    sms: int

    def __init__(self, gigabytes: int = 0, minutes: int = 0, sms: int = 0):
        self.gigabytes = int(gigabytes)
        self.minutes = int(minutes)
        self.sms = int(sms)

    def __repr__(self):
        return f'{self.__class__.__name__}(gigabytes={self.gigabytes}, minutes={self.minutes}, sms={self.sms})'

    def __ne__(self, other: 'Summary'):
        return self.minutes != other.minutes and self.gigabytes != other.gigabytes and self.sms != other.sms

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
