from cstruct import CStructMeta, CStruct, BIG_ENDIAN


class eTRVProperty:
    def __init__(self, name):
        self.name = name

    def __set_name__(self, owner, name):
        self.name = name

    def get_data_object(self, device):
        return device.fields[self.name]

    def __get__(self, device: 'eTRVDevice', instance_type=None):
        return self.get_data_object(device).retrieve(device)

    def __set__(self, device: 'eTRVDevice', value) -> None:
        self.get_data_object(device).update(device, value)
