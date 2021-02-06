from typing import List

from tele2client.containers import Lot, LotInfo, LotVolume
from tele2client.enums import LotType, Unit
from tele2client.wrappers.logger import LoggerWrap

import configs
from containers import Summary


class LotController(object):
    _prices_config: configs.MinLotPrice

    def __init__(self, prices_config: configs.MinLotPrice):
        self._prices_config = prices_config

    def create_objects_by_summary(self, summary: Summary) -> List[Lot]:
        lots = []
        gigabyte_price = self._prices_config.gigabyte
        for i in range(summary.gigabytes):
            lots.append(Lot(
                type=LotType.INTERNET,
                volume=LotVolume(gigabyte_price.count, Unit.GIGABYTES),
                cost=gigabyte_price.cost
            ))

        minutes_price = self._prices_config.minutes
        lot_count = summary.minutes  # minutes_price.count
        for i in range(lot_count):
            lots.append(Lot(
                type=LotType.VOICE,
                volume=LotVolume(minutes_price.count, Unit.MINUTES),
                cost=minutes_price.cost
            ))

        sms_price = self._prices_config.minutes
        lot_count = summary.sms  # sms_price.count
        for i in range(lot_count):
            lots.append(Lot(
                type=LotType.SMS,
                volume=LotVolume(sms_price.count, Unit.SMS),
                cost=sms_price.cost
            ))

        return lots

    def get_summary_for_create_lots(self, need_sell: Summary, sold_lots: List[LotInfo], active_lots: List[LotInfo],
                                    rests: Summary) -> Summary:
        summary = Summary()
        summary.set(need_sell)

        summary.decrement(self._create_summary_by_lots_info(sold_lots))
        summary.decrement(self._create_summary_by_lots_info(active_lots))

        return self._normalize_summary(summary, rests)

    def _create_summary_by_lots_info(self, lots_info: List[LotInfo]) -> Summary:
        summary = Summary()
        for lot_info in lots_info:
            self._increment_summary_by_lot_info(summary, lot_info)

        return summary

    def _increment_summary_by_lot_info(self, summary: Summary, lot_info: LotInfo):
        lot_type = lot_info.type
        if lot_type == LotType.INTERNET:
            summary.gigabytes += int(self._get_gigabyte_count(lot_info.volume))
        elif lot_type == LotType.VOICE:
            summary.minutes += int(self._get_minute_count(lot_info.volume))
        elif lot_type == LotType.SMS:
            summary.sms += lot_info.volume.count

    @staticmethod
    def _get_gigabyte_count(lot_volume: LotVolume) -> float:
        unit = lot_volume.unit
        if unit == Unit.GIGABYTES.value:
            return lot_volume.count
        if unit == Unit.MEGABYTES.value:
            return lot_volume.count / 1024
        LoggerWrap().get_logger().error(f'Неизвестная единица измерения значения в лоте: {lot_volume}')
        return 0.0

    @staticmethod
    def _get_minute_count(lot_volume: LotVolume) -> float:
        unit = lot_volume.unit
        if unit == Unit.MINUTES.value:
            return lot_volume.count
        LoggerWrap().get_logger().error(f'Неизвестная единица измерения значения в лоте: {lot_volume}')
        return 0.0

    @staticmethod
    def _normalize_summary(summary: Summary, rests_summary: Summary) -> Summary:
        new_summary = Summary()
        new_summary.gigabyte_count = min(summary.gigabytes, rests_summary.gigabytes)
        new_summary.minute_count = min(summary.minutes, rests_summary.minutes)
        new_summary.sms_count = min(summary.sms, rests_summary.sms)
        return new_summary
