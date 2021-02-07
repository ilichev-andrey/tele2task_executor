from typing import NamedTuple, Dict


class Price(NamedTuple):
    count: int
    cost: int


class MinLotPrice(NamedTuple):
    gigabyte: Price
    minutes: Price
    sms: Price


class LotConfig(NamedTuple):
    internet_life_time_minutes: int
    voice_life_time_minutes: int
    sms_life_time_minutes: int
    prices: MinLotPrice


class TaskConfig(NamedTuple):
    execution_interval_seconds: int


class ServerConfig(NamedTuple):
    host: str
    port: int


class Config(NamedTuple):
    log_file: str
    task: TaskConfig
    lot: LotConfig
    server: ServerConfig


def load_config(data: Dict) -> Config:
    """
    :raises
        KeyError если отсутствует параметр в конфиге
    """

    lot_data = data['lot']
    prices_data = lot_data['prices']
    server_data = data['server']
    return Config(
        log_file=data['log_file'],
        task=TaskConfig(execution_interval_seconds=data['task']['execution_interval_seconds']),
        lot=LotConfig(
            internet_life_time_minutes=lot_data['internet_life_time_minutes'],
            voice_life_time_minutes=lot_data['voice_life_time_minutes'],
            sms_life_time_minutes=lot_data['sms_life_time_minutes'],
            prices=MinLotPrice(
                gigabyte=Price(count=prices_data['gigabyte']['count'], cost=prices_data['gigabyte']['cost']),
                minutes=Price(count=prices_data['minutes']['count'], cost=prices_data['minutes']['cost']),
                sms=Price(count=prices_data['sms']['count'], cost=prices_data['sms']['cost'])
            )
        ),
        server=ServerConfig(host=server_data['host'], port=server_data['port'])
    )
