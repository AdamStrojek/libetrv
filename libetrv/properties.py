from cstruct import CStructMeta, CStruct, BIG_ENDIAN


class eTRVProperty:
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
