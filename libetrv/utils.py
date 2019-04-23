import struct
from functools import wraps

import xxtea


def etrv_read(handler, send_pin=False, cstruct_cls=None):
    def decorator(func):
        @wraps(func)
        def wrapper(etrv):
            if not etrv.is_connected():
                etrv.connect(send_pin)
            data = etrv.ble_device.readCharacteristic(handler)
            data = etrv_decode(data, etrv.secret)
            # TODO switch to type hints
            # https://docs.python.org/3.5/library/typing.html#typing.get_type_hints
            if cstruct_cls is not None:
                cstruct = cstruct_cls()
                cstruct.unpack(data)
                return func(etrv, cstruct)
            return func(etrv, data)
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
