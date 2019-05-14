import enum

from .properties import eTRVData, eTRVSingleData
from .fields import eTRVField, TemperatureField, UTCDateTimeField, LocalDateTimeField, EnumField


class BatteryData(eTRVSingleData):
    battery = eTRVField(read_only=True)
    class Meta:
        structure = {
            0x10: """
                unsigned char battery;
            """,
        }
        use_encoding = False
        read_only = True
        direct_field = 'battery'


class ScheduleMode(enum.Enum):
    MANUAL = 0
    SCHEDULED = 1
    VACATION = 2


class SettingsData(eTRVData):
    frost_protection_temperature = TemperatureField()
    schedule_mode = EnumField(enum_class=ScheduleMode)
    vacation_temperature = TemperatureField()
    vacation_from = UTCDateTimeField()
    vacation_to = UTCDateTimeField()

    class Meta:
        structure = {
            0x2a: """
                unsigned char unknow1[3];
                unsigned char frost_protection_temperature;
                unsigned char schedule_mode;
                unsigned char vacation_temperature; 
                int vacation_from;
                int vacation_to;
                unsigned char unknow2[2];
            """
        }


class TemperatureData(eTRVData):
    room_temperature = TemperatureField(read_only=True)
    set_point_temperature = TemperatureField(auto_save=True)

    class Meta:
        structure = {
            0x2d: """
                unsigned char room_temperature;
                unsigned char set_point_temperature;
                unsigned char padding[6];
            """
        }


class CurrentTimeData(eTRVSingleData):
    current_time = LocalDateTimeField('time_local', tz_field='time_offset')

    class Meta:
        structure = {
            0x36: """
                int time_local;
                int time_offset;
            """
        }
        direct_field = 'current_time'


class SecretKeyData(eTRVSingleData):
    key = eTRVField(read_only=True)

    class Meta:
        structure = {
            0x3f: """
                char key[16];
            """
        }
        use_encoding = False


# class DaySchedule(eTRVData):
#     __struct__ = """
#         unsigned char _data[6];
#     """


# class ScheduleStruct(eTRVData):
#     __struct__ = """
#         unsigned char _home_temperature;
#         unsigned char _away_temperature;
#         struct DaySchedule _schedule[7];
#     """
