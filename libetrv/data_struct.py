import cstruct
import enum
from typing import Optional, Any, Union, Dict

from .utils import etrv_read_data, etrv_write_data

class eTRVField:
    def __init__(self, handler=None, name=None, read_only=False, auto_save=False):
        self.handler = handler
        self.read_only = read_only
        self.auto_save = auto_save
        self.name = name

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name

    def __get__(self, data: 'eTRVData', instance_type=None):
        raw_value = None
        if len(data.raw_data) == 1 and self.handler is None:
            # Take first and only field
            handler, raw_data = next(iter(data.raw_data.items()))
            raw_value = getattr(raw_data, self.name)
        else:
            raw_data = data.raw_data[self.handler]
            raw_value = getattr(raw_data, self.name)
        return self.from_raw_value(raw_value, data)

    def __set__(self, data: 'eTRVData', value):
        if self.read_only:
            raise AttributeError("field '{}' is read-only".format(self.name))

        value = self.to_raw_value(value, data)

        if len(data.raw_data) == 1 and self.handler is None:
            # Take first and only field
            handler, raw_data = next(iter(data.raw_data.items()))
            raw_data.is_changed = True
            raw_value = setattr(raw_data, self.name, value)
        else:
            raw_data = data.raw_data[self.handler]
            raw_data.is_changed = True
            raw_value = setattr(raw_data, self.name, value)

        # if self.auto_save:
        #     property.save()

    def from_raw_value(self, raw_value, data):
        return raw_value

    def to_raw_value(self, value, data):
        return value


class eTRVDataMeta(type):
    def __new__(mcls, name, bases, attrs):
        cls = super(eTRVDataMeta, mcls).__new__(mcls, name, bases, attrs)
        for attr, obj in attrs.items():
            if isinstance(obj, eTRVField):
                obj.__set_name__(cls, attr)
        return cls


class eTRVData(metaclass=eTRVDataMeta):
    class Meta:
        structure = None  # type: Dict[int, str]
        send_pin = True
        use_encoding = True
        read_only = False

    def __init__(self, device):
        self.device = device
        # TODO Should we switch to frozendict?
        self.raw_data = {}
        for handler, struct in self.Meta.structure.items():
            class RawDataStruct(cstruct.CStruct):
                __byte_order__ = cstruct.BIG_ENDIAN
                __struct__ = struct
                is_populated = False
                is_changed = False

            self.raw_data[handler] = RawDataStruct()

    def retrieve(self):
        if not self.is_populated:
            self.read()

        return self.retrieve_object(self.device)

    def retrieve_object(self, device):
        return self
    
    def update(self, data):
        if self.Meta.read_only:
            raise AttributeError('this attribute is read-only')

    def update_object(self, device, data):
        pass

    @property
    def is_populated(self):
        return all(map(lambda obj: obj.is_populated, self.raw_data.values()))

    @property
    def is_changed(self):
        return any(map(lambda obj: obj.is_populated, self.raw_data.values()))

    def read(self, handlers = None):
        """
        If handlers are None it will use all
        """
        for handler, struct in self.raw_data.items():
            send_pin = getattr(self.Meta, 'send_pin', eTRVData.Meta.send_pin)
            use_encoding = getattr(self.Meta, 'use_encoding', eTRVData.Meta.use_encoding)
            data = etrv_read_data(self.device, handler, send_pin, use_encoding)
            struct.unpack(data)
            struct.is_populated = True
            struct.is_changed = False

    def save(self):
        if self.Meta.read_only:
            raise AttributeError('this attribute is read-only')

        results = []

        for handler, struct in self.raw_data.items():
            data = struct.pack()
            result = etrv_write_data(self.device, handler, data, self.Meta.send_pin, self.Meta.use_encoding)
            if result:
                struct.is_changed = False
            results.append(result)

        return all(results)


class eTRVSingleData(eTRVData):
    direct_field = None

    def get_direct_field(self):
        if self.direct_field is None:
            raise AttributeError('Field direct field should be defined')

    def retrieve_object(self):
        return getattr(self, self.get_direct_field())


class ScheduleMode(enum.IntEnum):
    MANUAL = 0
    SCHEDULED = 1
    VACATION = 2


class SettingsStruct(eTRVData):
    class Meta(eTRVData.Meta):
        __struct__ = """
            unsigned char unknow1[3];
            unsigned char frost_protection_temperature;
            unsigned char schedule_mode;
            unsigned char vacation_temperature; 
            int vacation_from;
            int vacation_to;
            unsigned char unknow2[2];
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
