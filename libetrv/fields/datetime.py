from datetime import datetime, timedelta, timezone

from .base import eTRVField


class UTCDateTimeField(eTRVField):
    def from_raw_value(self, raw_value, property):
        if raw_value == 0:
            return None
        return datetime.utcfromtimestamp(raw_value)

    def to_raw_value(self, value, property):
        if value is None:
            return 0
        elif isinstance(value, datetime):
            return int(value - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()
        elif isinstance(value, int):
            return value
        
        raise ValueError('type not supported')


class LocalDateTimeField(eTRVField):
    def __init__(self, *args, tz_field, **kwargs):
        super().__init__(*args, **kwargs)
        self.tz_field = tz_field

    def from_raw_value(self, raw_value, property):
        if raw_value == 0:
            return None
        return datetime.fromtimestamp(
            raw_value,
            tz=timezone(timedelta(seconds=getattr(property, self.tz_field))
        ))

    def to_raw_value(self, value, property):
        setattr(property, self.tz_field, 0)
        if value is None:
            return 0
        elif isinstance(value, datetime):
            utc_offset = value.utcoffset()
            if utc_offset is not None:
                setattr(property, self.tz_field, utc_offset.total_seconds())
            return value.timestamp()
        elif isinstance(value, int):
            return value
        
        raise ValueError('type not supported')
