from collections import namedtuple
from typing import List

from .base import eTRVField


TimeSchedule = namedtuple("TimeSchedule", ['is_away', 'hour', 'minute'])


def fix_raw_time(raw_time: int) -> int:
    result = max(0, min(48, raw_time))
    return result


class DailyScheduleField(eTRVField):
    def from_raw_value(self, raw_value, property):
        items = []
        is_away = False

        if raw_value[0] != 0:
            items.append(TimeSchedule(is_away, 0, 0))
            is_away = not is_away

        for raw_time in raw_value:
            raw_time = fix_raw_time(raw_time)
            hour, half = divmod(raw_time, 2)
            item = TimeSchedule(is_away, hour, [0, 30][half])
            is_away = not is_away
            items.append(item)
            if raw_time >= 48:
                break
        
        return items

    def to_raw_value(self, value: List[TimeSchedule], property):
        result = [0]*6
        for i, entry in enumerate(value):
            result[i] = entry.hour*2 + int(entry.minute >= 30)
        return result
