from collections.abc import Iterable
from functools import wraps
from typing import Union, get_type_hints, TYPE_CHECKING

import xxtea

if TYPE_CHECKING:
    from .device import eTRVDevice


def etrv_read_data(device: 'eTRVDevice', handlers, send_pin: bool, decode: bool) -> bytes:
    if not device.is_connected():
        device.connect(send_pin)
    complete_data = bytearray()

    if not isinstance(handlers, Iterable):
        handlers = [handlers]

    for handler in handlers:
        data = device.ble_device.readCharacteristic(handler)
        if decode:
            data = etrv_decode(data, device.secret)
        complete_data += data
    
    return bytes(complete_data)


def etrv_write_data(device: 'eTRVDevice', handler, data: bytes, send_pin: bool, encode: bool):
    if encode:
        data = etrv_encode(data, device.secret)
    if not device.is_connected():
        device.connect(send_pin)
    ret = device.ble_device.writeCharacteristic(handler, data, True)
    return ret


def etrv_read(handlers: Union[int, Iterable], send_pin: bool = False, decode: bool = True):
    if not isinstance(handlers, Iterable):
        handlers = [handlers]
    def decorator(func):
        @wraps(func)
        def wrapper(etrv):
            data = etrv_read_data(etrv, handlers, send_pin, decode)
            hints = get_type_hints(func)
            cstruct_cls = hints['data']
            if cstruct_cls is not None:
                cstruct = cstruct_cls()
                cstruct.unpack(data)
                return func(etrv, cstruct)
            return func(etrv, data)
        return wrapper
    return decorator


def etrv_write(handler: int, send_pin: bool = False, encode: bool = True):
    def decorator(func):
        @wraps(func)
        def wrapper(etrv, *args):
            data = func(etrv, *args)
            if hasattr(data, 'pack'):
                data = data.pack()
            return etrv_write_data(etrv, handler, data, send_pin, encode)
        return wrapper
    return decorator


def etrv_decode(data: bytes, key: bytes) -> bytes:
    data = etrv_reverse_chunks(data)
    data = xxtea.decrypt(bytes(data), key, padding=False)
    data = etrv_reverse_chunks(data)
    return data


def etrv_encode(data: bytes, key: bytes) -> bytes:
    data = etrv_reverse_chunks(data)
    data = xxtea.encrypt(bytes(data), key, padding=False)
    data = etrv_reverse_chunks(data)
    return data


def etrv_reverse_chunks(data: bytes):
    result = bytearray()
    for i in range(0, len(data), 4):
        result += data[i:i+4][::-1]
    return result
