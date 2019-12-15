from .base import eTRVField


class BitField(eTRVField):
    def __init__(self, *args, bit_position, **kwargs):
        super().__init__(*args, **kwargs)
        self.mask = ( 1 << bit_position )

    def from_raw_value(self, raw_value, property):
        return ( raw_value & self.mask ) == self.mask

    def to_raw_value(self, value, property):
        if len(property.raw_data) == 1 and self.handler is None:
            # Take first and only field
            handler, raw_data = next(iter(property.raw_data.items()))
            raw_value = getattr(raw_data, self.name)
        else:
            raw_data = property.raw_data[self.handler]
            raw_value = getattr(raw_data, self.name)
        
        raw_value_new = (raw_value & (~self.mask))
        if value:
            raw_value_new |= self.mask
        return int(raw_value_new)
