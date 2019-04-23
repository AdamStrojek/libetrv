import struct
from collections import Iterable
from functools import wraps
from typing import Union, get_type_hints

import xxtea


def etrv_read(handlers: Union[int, Iterable], send_pin: bool = False, decode: bool = True):
    if not isinstance(handlers, Iterable):
        handlers = [handlers]
    def decorator(func):
        @wraps(func)
        def wrapper(etrv):
            if not etrv.is_connected():
                etrv.connect(send_pin)
            complete_data = bytearray()

            for handler in handlers:
                data = etrv.ble_device.readCharacteristic(handler)
                if decode:
                    data = etrv_decode(data, etrv.secret)
                complete_data += data
            hints = get_type_hints(func)
            cstruct_cls = hints['data']
            if cstruct_cls is not None:
                cstruct = cstruct_cls()
                cstruct.unpack(complete_data)
                return func(etrv, cstruct)
            return func(etrv, complete_data)
        return wrapper
    return decorator


def etrv_write(handler: int, send_pin: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(etrv, *args):
            data = func(etrv, *args)
            if hasattr(data, 'pack'):
                data = data.pack()
            data = etrv_encode(data, etrv.secret)
            if not etrv.is_connected():
                etrv.connect(send_pin)
            ret = etrv.ble_device.writeCharacteristic(handler, data, True)
            return ret
        return wrapper
    return decorator


def etrv_repack(data: bytes, format: str):
    return struct.pack(format, *struct.unpack('>'+format, data))


def etrv_decode(data: bytes, key: bytes) -> bytes:
    data = etrv_reverse_chunks(data)
    data = xxtea.decrypt(data, key, padding=False, rounds=32)
    data = etrv_reverse_chunks(data)
    return data


def etrv_encode(data: bytes, key: bytes) -> bytes:
    data = etrv_reverse_chunks(data)
    data = xxtea.encrypt(data, key, padding=False, rounds=32)
    data = etrv_reverse_chunks(data)
    return data


def etrv_reverse_chunks(data: bytes):
    result = []
    for i in range(0, len(data), 4):
        result.append(data[i:i+4][::-1])
    return b''.join(result)
