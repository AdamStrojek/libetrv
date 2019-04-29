from collections import namedtuple

from .data_struct import ScheduleStruct


TimeSchedule = namedtuple("TimeSchedule", ['is_away', 'hour', 'minute'])


class Schedule:
    def __init__(self):
        self.home_temperature = None
        self.away_temperature = None
        self.schedule = []
        for _ in range(7):
            self.schedule.append([])

    @classmethod
    def from_struct(cls, data: ScheduleStruct):
        obj = cls()
        obj.raw_data = data
        obj.home_temperature = data.home_temperature * .5
        obj.away_temperature = data.away_temperature * .5
        for weekday, schedule in enumerate(data.schedule):
            is_away = False
            for raw_time in schedule.data:
                hour, half = divmod(raw_time, 2)
                item = TimeSchedule(is_away, hour, [0, 30][half])
                is_away = not is_away
                obj.schedule[weekday].append(item)
                if raw_time >= 48:
                    break
        return obj
