from .base import eTRVField


class HexField(eTRVField):
    def from_raw_value(self, raw_value, data):
        return bytes(raw_value).hex()

    def to_raw_value(self, value, data):
        return bytes.fromhex(value)


class TextField(eTRVField):
    def __init__(self, *args, max_length, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = max_length

    def from_raw_value(self, raw_value, data):
        return raw_value.decode('utf8').strip('\0')
    
    def to_raw_value(self, value, data):
        return str.encode(value[:self.max_length], encoding='utf8').ljust(self.max_length, b'\0')
