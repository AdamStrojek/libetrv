from .base import eTRVField


class EnumField(eTRVField):
    def __init__(self, *args, enum_class, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_class = enum_class

    def from_raw_value(self, raw_value, data):
        return self.enum_class(raw_value)

    def to_raw_value(self, value, data):
        if not isinstance(value, self.enum_class):
            raise AttributeError('Provided value is wrong type')
        return value.value
