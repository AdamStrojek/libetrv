from .base import eTRVField


class TemperatureField(eTRVField):
    def from_raw_value(self, raw_value, property):
        return raw_value * .5

    def to_raw_value(self, value, property):
        return int(value*2)
