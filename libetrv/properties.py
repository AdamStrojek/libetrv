from cstruct import CStructMeta, CStruct, BIG_ENDIAN


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
