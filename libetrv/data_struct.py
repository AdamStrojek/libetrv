import cstruct
import enum


class ScheduleMode(enum.IntEnum):
    MANUAL = 0
    SCHEDULED = 1
    VACATION = 2


class SettingsStruct(cstruct.CStruct):
    __byte_order__ = cstruct.BIG_ENDIAN
    __struct__ = """
        unsigned char unknow1[3];
        unsigned char frost_protection_temperature;
        unsigned char schedule_mode;
        unsigned char vacation_temperature; 
        int vacation_from;
        int vacation_to;
        unsigned char unknow2[2];
    """


class TemperatureStruct(cstruct.CStruct):
    __byte_order__ = cstruct.BIG_ENDIAN
    __struct__ = """
        unsigned char room_temperature;
        unsigned char set_point_temperature;
        unsigned char padding[6];
    """


class TimeStruct(cstruct.CStruct):
    __byte_order__ = cstruct.BIG_ENDIAN
    __struct__ = """
        int time_local;
        int time_offset;
    """


class BatteryStruct(cstruct.CStruct):
    __byte_order__ = cstruct.BIG_ENDIAN
    __struct__ = """
        unsigned char battery;
    """


class DaySchedule(cstruct.CStruct):
    __byte_order__ = cstruct.BIG_ENDIAN
    __struct__ = """
        unsigned char data[6];
    """


class ScheduleStruct(cstruct.CStruct):
    __byte_order__ = cstruct.BIG_ENDIAN
    __struct__ = """
        unsigned char home_temperature;
        unsigned char away_temperature;
        struct DaySchedule schedule[7];
    """
