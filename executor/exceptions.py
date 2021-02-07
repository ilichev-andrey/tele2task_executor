class BaseTele2TaskExecutorException(Exception):
    """Базовое исключение данного модуля"""
    pass


class CommandException(BaseTele2TaskExecutorException):
    """Базовое искличение для выполнения команды"""
    pass


class UnknownCommand(CommandException):
    """Получена неизвестная команда"""
    pass


class InvalidFormatCommand(CommandException):
    """Получена команда с невалидным форматом данных"""
    pass
