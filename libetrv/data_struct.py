import cstruct
import enum

from .utils import etrv_read_data, etrv_write_data

class eTRVField:
    def __init__(self, field=None, read_only=False, auto_save=False):
        self.field = field
        self.read_only = read_only
        self.auto_save = auto_save
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name
        if self.field is None:
            self.field = name

    def __get__(self, data: 'eTRVData', instance_type=None):
        return self.from_raw_value(data, property.__values__[self.field], property)

    def __set__(self, data: 'eTRVData', value):
        if self.read_only:
            raise AttributeError("field '{}' is read-only".format(self.name))

        result = self.to_raw_value(value, property)
        property.__values__[self.field] = result
        property.is_changed = True

        if self.auto_save:
            property.save()

    def from_raw_value(self, raw_value, data):
        return raw_value

    def to_raw_value(self, value, data):
        return value


class eTRVData:
    class Meta:
        structure = None  # type: dict[int] = str
        send_pin = True
        use_encoding = True
        read_only = False

    def __init__(self, device=None):
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

    def retrieve(self, device: 'eTRVDevice'):
        if not self.is_populated:
            self.read(device)

        return self.retrieve_object(device)

    def retrieve_object(self, device):
        return self
    
    def update(self, device: 'eTRVDevice', data):
        pass

    def update_object(self, device, data):
        if self.Meta.read_only:
            raise AttributeError('this attribute is read-only')

    @property
    def is_populated(self):
        return all(filter(lambda obj: obj.is_populated, self.raw_data.values()))

    @property
    def is_changed(self):
        return any(filter(lambda obj: obj.is_populated, self.raw_data.values()))

    def read(self, device: 'eTRVDevice', handlers = None):
        """
        If handlers are None it will use all
        """
        for handler, struct in self.raw_data.items():
            data = etrv_read_data(device, handler, self.Meta.send_pin, self.Meta.use_encoding)
            struct.unpack(data)
            struct.is_populated = True
            struct.is_changed = False

    def save(self, device: 'eTRVDevice'):
        if self.Meta.read_only:
            raise AttributeError('this attribute is read-only')

        results = []

        for handler, struct in self.raw_data.items():
            data = struct.pack()
            result = etrv_write_data(device, handler, data, self.Meta.send_pin, self.Meta.use_encoding)
            if result:
                struct.is_changed = False
            results.append(result)

        return all(results)


class eTRVSingleData(eTRVData):
    direct_field = None

    def get_direct_field(self):
        if self.direct_field is None:
            raise AttributeError('Field direct field should be defined')

    def retrieve_object(self, device):
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
