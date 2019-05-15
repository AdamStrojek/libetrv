
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

        if self.auto_save:
            data.save()

    def from_raw_value(self, raw_value, data):
        return raw_value

    def to_raw_value(self, value, data):
        return value
