from cstruct import CStructMeta, CStruct, BIG_ENDIAN

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


class eTRVPropertyMeta(CStructMeta):
    def __new__(mcls, name, bases, attrs):
        cls = super(eTRVPropertyMeta, mcls).__new__(mcls, name, bases, attrs)
        for attr, obj in attrs.items():
            if isinstance(obj, eTRVField):
                obj.__set_name__(cls, attr)
        return cls


class eTRVProperty(CStruct, metaclass=eTRVPropertyMeta):
    __byte_order__ = BIG_ENDIAN
    handler = 0
    send_pin = True
    use_encoding = True
    read_only = False
    direct_field = None

    def __init__(self, data: bytes = None, **kwargs):
        super().__init__(string=data, **kwargs)
        self.populated = False
        self.is_changed = False
        self.device = None

    def __set_device__(self, device: 'eTRVDevice'):
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

    def __get__(self, device: 'eTRVDevice', instance_type=None):
        if not self.populated:
            self.read(device)

        if self.direct_field is None:
            return self
        else:
            return getattr(self, self.direct_field)

    def __set__(self, device: 'eTRVDevice', value):
        if self.read_only:
            raise AttributeError('this attribute is read-only')

        self.is_changed = True
        
        if self.direct_field is None:
            # This require modified version of cstruct
            self.__values__.update(value.__values__)
        else:
            setattr(self, self.direct_field, value)
