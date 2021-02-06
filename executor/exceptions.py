class BaseTele2TaskExecutorException(Exception):
    """Базовое исключение данного модуля"""
    pass


class InvalidFormatCommand(BaseTele2TaskExecutorException):
    """Получена команда с невалидным форматом данных"""
    pass
