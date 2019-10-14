from collections import namedtuple
from typing import List, Generator

from .base import eTRVField


TimeSchedule = namedtuple("TimeSchedule", ['is_away', 'hour', 'minute'])


def fix_raw_time(raw_time: int) -> int:
    result = max(0, min(48, raw_time))
    return result


class DailyScheduleField(eTRVField):
    def from_raw_value(self, raw_value, property) -> Generator[TimeSchedule]:
        """
        RAW data from device have it own format. It is array of 6 short integers (char),
        by default 0 filled. Each value is saving information about hour and half. To
        calculate proper hour you need to divide it by 2, all halfs are 30 minutes.
        Each odd item starts home temperature.
        Each even item starts away temperature.
        First record do not need to start from midnight, it can be any hour. All values
        above 48 are not possible to assigne, because this is above 24h clock.
        """
        for index, raw_time in enumerate(raw_value):
            raw_time = fix_raw_time(raw_time)
            hour, half = divmod(raw_time, 2)
            yield TimeSchedule(bool(index/2), hour, [0, 30][half])
            if raw_time >= 48:
                break

    def to_raw_value(self, value: List[TimeSchedule], property):
        """
        This method will totally ignore `is_away` attribute
        """
        result = [0]*6
        value = value[:6]  # More then 6 values will be ignored
        for i, entry in enumerate(value):
            result[i] = entry.hour*2 + int(entry.minute >= 30)
        return result
