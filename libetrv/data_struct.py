import cstruct
import enum

from .utils import etrv_read_data, etrv_write_data

class eTRVField:
    def __init__(self, field=None, read_only=False, auto_save=False):
        self.field = field
        self.read_only = read_only
        self.auto_save = auto_save

    def __set_name__(self, owner, name):
        self.name = name
        if self.field is None:
            self.field = name

    def __get__(self, property: 'eTRVProperty', instance_type=None):
        return self.from_raw_value(property.__values__[self.field], property)

    def __set__(self, property: 'eTRVProperty', value):
        if self.read_only:
            raise AttributeError("field '{}' is read-only".format(self.name))

        result = self.to_raw_value(value, property)
        property.__values__[self.field] = result
        property.is_changed = True

        if self.auto_save:
            property.save()

    def from_raw_value(self, raw_value, property):
        return raw_value

    def to_raw_value(self, value, property):
        return value


class eTRVPropertyMeta(cstruct.CStructMeta):
    def __new__(mcls, name, bases, attrs):
        cls = super(eTRVPropertyMeta, mcls).__new__(mcls, name, bases, attrs)
        for attr, obj in attrs.items():
            if isinstance(obj, eTRVField):
                obj.__set_name__(cls, attr)
        return cls


class eTRVData(cstruct.CStruct):
    __byte_order__ = cstruct.BIG_ENDIAN

    def __init__(self, device, data=None, **kargs):
        super().__init__(string=data, **kargs)
        self.device = device
        
    def unpack(self, string):
        result = super().unpack(string)
        self.populated = True
        self.is_changed = False
        return result

    def read(self, device: 'eTRVDevice'):
        data = etrv_read_data(device, self.handler, self.send_pin, self.use_encoding)
        self.unpack(data)

    def save(self, device: 'eTRVDevice'):
        data = self.pack()
        result = etrv_write_data(device, self.handler, data, self.send_pin, self.use_encoding)
        if result:
            self.is_changed = False
        return result

class ScheduleMode(enum.IntEnum):
    MANUAL = 0
    SCHEDULED = 1
    VACATION = 2


class SettingsStruct(eTRVData):
    __struct__ = """
        unsigned char _unknow1[3];
        unsigned char _frost_protection_temperature;
        unsigned char _schedule_mode;
        unsigned char _vacation_temperature; 
        int _vacation_from;
        int _vacation_to;
        unsigned char _unknow2[2];
    """




class TemperatureStruct(eTRVData):
    __struct__ = """
        unsigned char _room_temperature;
        unsigned char _set_point_temperature;
        unsigned char _padding[6];
    """


class TimeStruct(eTRVData):
    __struct__ = """
        int _time_local;
        int _time_offset;
    """


class BatteryStruct(eTRVData):
    __struct__ = """
        unsigned char _battery;
    """


class DaySchedule(eTRVData):
    __struct__ = """
        unsigned char _data[6];
    """


class ScheduleStruct(eTRVData):
    __struct__ = """
        unsigned char _home_temperature;
        unsigned char _away_temperature;
        struct DaySchedule _schedule[7];
    """
