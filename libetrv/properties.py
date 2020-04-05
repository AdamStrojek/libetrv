from cstruct import CStructMeta, CStruct, BIG_ENDIAN
from typing import Optional, Any, Union, Dict

from .fields import eTRVField
from .utils import etrv_read_data, etrv_write_data


class eTRVProperty:
    def __init__(self, data_struct, **init_kwargs):
        self.data_struct = data_struct
        self.init_kwargs = init_kwargs

    def __set_name__(self, owner, name):
        self.name = name

    def get_data_object(self, device):
        if self.name not in device.fields:
            device.fields[self.name] = self.data_struct(device=device, **self.init_kwargs)
        return device.fields[self.name]

    def __get__(self, device: 'eTRVDevice', instance_type=None):
        return self.get_data_object(device).retrieve()

    def __set__(self, device: 'eTRVDevice', value) -> None:
        self.get_data_object(device).update(value)


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
            class RawDataStruct(CStruct):
                __byte_order__ = BIG_ENDIAN
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
        read_only = getattr(self.Meta, 'read_only', eTRVData.Meta.read_only)
        if read_only:
            raise AttributeError('this attribute is read-only')

        self.update_object(self.device, data)

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
        send_pin = getattr(self.Meta, 'send_pin', eTRVData.Meta.send_pin)
        use_encoding = getattr(self.Meta, 'use_encoding', eTRVData.Meta.use_encoding)
        for handler, struct in self.raw_data.items():
            data = etrv_read_data(self.device, handler, send_pin, use_encoding)
            struct.unpack(data)
            struct.is_populated = True
            struct.is_changed = False

    def save(self):
        if getattr(self.Meta, 'read_only', eTRVData.Meta.read_only):
            raise AttributeError('this attribute is read-only')

        results = []

        send_pin = getattr(self.Meta, 'send_pin', eTRVData.Meta.send_pin)
        use_encoding = getattr(self.Meta, 'use_encoding', eTRVData.Meta.use_encoding)

        for handler, struct in self.raw_data.items():
            data = struct.pack()
            result = etrv_write_data(self.device, handler, data, send_pin,use_encoding)
            if result:
                struct.is_changed = False
            results.append(result)

        return all(results)

    def invalidate(self):
        for struct in self.raw_data.values():
            struct.is_populated = False
            struct.is_changed = False


class eTRVSingleData(eTRVData):

    def get_direct_field(self):
        direct_field = getattr(self.Meta, 'direct_field', None)
        if direct_field is None:
            raise AttributeError('Field "direct_field" should be defined or "get_direct_field" should be implemented')
        return direct_field

    def retrieve_object(self, device):
        return getattr(self, self.get_direct_field())

    def update_object(self, device, data):
        return setattr(self, self.get_direct_field(), data)

    class Meta:
        direct_field = None
