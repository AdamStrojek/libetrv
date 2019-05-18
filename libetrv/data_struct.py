import enum

from .properties import eTRVData, eTRVSingleData
from .fields import eTRVField, TemperatureField, UTCDateTimeField, LocalDateTimeField, EnumField, \
    HexField, TextField, DailyScheduleField


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
    VACATION = 3
    HOLD = 5


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
                unsigned char set_point_temperature;
                unsigned char room_temperature;
                unsigned char padding[6];
            """
        }


class NameData(eTRVSingleData):
    name = TextField(max_length=16, auto_save=True)

    class Meta:
        structure = {
            0x30: """
                char name[16];
            """
        }
        direct_field = 'name'


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
    key = HexField(read_only=True)

    class Meta:
        structure = {
            0x3f: """
                char key[16];
            """
        }
        use_encoding = False


class ScheduleData(eTRVData):
    home_temperature = TemperatureField(0x45)
    away_temperature = TemperatureField(0x45)

    monday = DailyScheduleField(0x45)
    tuesday = DailyScheduleField(0x45)
    wednesday = DailyScheduleField(0x45)
    thursday = DailyScheduleField(0x48)
    friday = DailyScheduleField(0x48)
    saturday = DailyScheduleField(0x4b)
    sunday = DailyScheduleField(0x4b)

    class Meta:
        structure = {
            0x45: """
                unsigned char home_temperature;
                unsigned char away_temperature;
                unsigned char monday[6];
                unsigned char tuesday[6];
                unsigned char wednesday[6];
            """,
            0x48: """
                unsigned char thursday[6];
                unsigned char friday[6];
            """,
            0x4b: """
                unsigned char saturday[6];
                unsigned char sunday[6];
            """,
        }
