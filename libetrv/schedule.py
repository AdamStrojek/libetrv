from collections import namedtuple

from .data_struct import ScheduleStruct
from .exceptions import ParsingError


TimeSchedule = namedtuple("TimeSchedule", ['is_away', 'hour', 'minute'])


def fix_raw_time(raw_time: int, fail_silently: bool = True) -> int:
    if raw_time < 0:
        result = 0
    elif raw_time > 48:
        result = 48
    
    if not fail_silently and result != raw_time:
        raise ParsingError("raw_time exeeded limit")
    
    return result


class Schedule:
    def __init__(self):
        self.home_temperature = None
        self.away_temperature = None
        self.schedule = []
        for _ in range(7):
            self.schedule.append([])

    @classmethod
    def from_struct(cls, data: ScheduleStruct, fail_silently: bool = True):
        obj = cls()
        obj.raw_data = data
        obj.home_temperature = data.home_temperature * .5
        obj.away_temperature = data.away_temperature * .5
        for weekday, schedule in enumerate(data.schedule):
            is_away = False
            for raw_time in schedule.data:
                raw_time = fix_raw_time(raw_time, fail_silently)
                hour, half = divmod(raw_time, 2)
                item = TimeSchedule(is_away, hour, [0, 30][half])
                is_away = not is_away
                obj.schedule[weekday].append(item)
                if raw_time >= 48:
                    break
        return obj
