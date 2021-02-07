from datetime import datetime, timedelta
from typing import List

from tele2client import time_utils, converter
from tele2client.client import Tele2Client
from tele2client.containers import LotInfo
from tele2client.enums import LotType, LotStatus, Unit
from tele2client.exceptions import BaseTele2ClientException
from tele2client.wrappers.logger import LoggerWrap

import configs
from containers import Summary
from lot.lot_controller import LotController


class LotManager(object):
    _config: configs.LotConfig
    _controller: LotController

    def __init__(self, config: configs.LotConfig):
        self._config = config
        self._controller = LotController(config.prices)

    async def create(self, summary: Summary, client: Tele2Client) -> List[LotInfo]:
        lots_for_create = self._controller.create_objects_by_summary(summary)
        lots = []
        for lot in lots_for_create:
            LoggerWrap().get_logger().info(f'Пересоздание лота: {lot}')
            try:
                lot_info = await client.create_lot(lot)
            except BaseTele2ClientException as e:
                LoggerWrap().get_logger().exception(str(e))
            else:
                lots.append(lot_info)

        return lots

    async def renew(self, lots: List[LotInfo], summary: Summary, client: Tele2Client) -> List[LotInfo]:
        sold_lots = await self._get_sold_lots(lots, client)
        deleted_lots = await self._delete_expired_lots(lots, client)
        active_lots = self._get_active_lots(lots, sold_lots, deleted_lots)
        rests = await self._get_sellable_rests(client)

        new_summary = self._controller.get_summary_for_create_lots(summary, sold_lots, active_lots, rests)
        active_lots.extend(await self.create(new_summary, client))
        return active_lots

    async def get_lots_for_sale(self, summary: Summary, client: Tele2Client) -> Summary:
        rests = await self._get_sellable_rests(client)
        LoggerWrap().get_logger().info(f'Получены остатки тарифа {rests}')
        return self._controller.get_summary_for_create_lots(summary, [], [], rests)

    @staticmethod
    async def _get_sellable_rests(client: Tele2Client) -> Summary:
        try:
            rests = await client.get_sellable_rests()
        except BaseTele2ClientException as e:
            LoggerWrap().get_logger().exception(str(e))
            raise

        summary = Summary()
        for remain in rests:
            if remain.unit == Unit.MINUTES:
                summary.increment_minutes(remain.value)
            elif remain.unit == Unit.MEGABYTES:
                summary.increment_gigabytes(converter.megabytes2gigabytes(remain.value))
            elif remain.unit == Unit.GIGABYTES:
                summary.increment_gigabytes(remain.value)
            elif remain.unit == Unit.SMS:
                summary.increment_sms(remain.value)
            else:
                LoggerWrap().get_logger().warning('Неизвестная единица измерения', remain)

        return summary

    @staticmethod
    async def _get_sold_lots(lots: List[LotInfo], client: Tele2Client) -> List[LotInfo]:
        try:
            all_lots = await client.get_lots()
        except BaseTele2ClientException as e:
            LoggerWrap().get_logger().exception(str(e))
            raise

        ids = set(lot.id for lot in lots)
        sold_lots = []
        for lot in all_lots:
            if lot.status != LotStatus.BOUGHT:
                continue
            if lot.id in ids:
                sold_lots.append(lot)

        return sold_lots

    @staticmethod
    def _get_active_lots(lots: List[LotInfo], sold_lots: List[LotInfo],
                         deleted_lots: List[LotInfo]) -> List[LotInfo]:
        inactive_lot_ids = set(lot.id for lot in sold_lots)
        inactive_lot_ids.update(lot.id for lot in deleted_lots)
        return [lot for lot in lots if lot.id not in inactive_lot_ids]

    async def _delete_expired_lots(self, lots: List[LotInfo], client: Tele2Client) -> List[LotInfo]:
        deleted_lots = []
        for lot in lots:
            if time_utils.is_expired(self._get_lot_deadline(lot)):
                LoggerWrap().get_logger().info(f'Удаление не проданного лота: {lot}')
                if await client.delete_lot(lot.id):
                    deleted_lots.append(lot)
                else:
                    LoggerWrap().get_logger().warning('Не удалось удалить лот', lot)
        return deleted_lots

    def _get_lot_deadline(self, lot: LotInfo) -> datetime:
        minutes = 0
        if lot.type == LotType.INTERNET:
            minutes = self._config.internet_life_time_minutes
        elif lot.type == LotType.VOICE:
            minutes = self._config.voice_life_time_minutes
        elif lot.type == LotType.SMS:
            minutes = self._config.sms_life_time_minutes
        else:
            LoggerWrap().get_logger().warning('Неизвестный тип лота', lot)
        return lot.create_dt + timedelta(minutes=minutes)
