from collections import namedtuple
from datetime import time

from .data_struct import ScheduleStruct


TimeSchedule = namedtuple("TimeSchedule", ['is_away', 'time'])


class Schedule:
    def __init__(self):
        self.home_temperature = None
        self.away_temperature = None
        self.schedule = [[]*7]
    
    @classmethod
    def from_struct(cls, data: ScheduleStruct):
        obj = cls()
        obj.raw_data = data
        obj.home_temperature = data.home_temperature * .5
        obj.away_temperature = data.away_temperature * .5
        for weekday, schedule in enumerate(data.schedule):
            is_away = False
            for raw_time in schedule:
                item = TimeSchedule()
                item.is_away = is_away
                hours, halfs = divmod(raw_time, 2)
                item.time = time(hours, [0, 30][halfs])
                is_away = not is_away
                obj.schedule[weekday].append(item)
                if hours >= 24:
                    break
        return obj
