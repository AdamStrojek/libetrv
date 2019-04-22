import struct
from functools import wraps

import xxtea


def etrv_read(handler, send_pin=False):
    def decorator(func):
        @wraps(func)
        def wrapper(etrv):
            if not etrv.is_connected():
                etrv.connect(send_pin)
            data = etrv.ble_device.readCharacteristic(handler)
            return func(etrv, data)
        return wrapper
    return decorator


def etrv_repack(data: bytes, format: str):
    return struct.pack(format, *struct.unpack('>'+format, data))


def etrv_decode(data: bytes, key: bytes):
    return xxtea.decrypt(data, key, padding=False, rounds=32)


def etrv_reverse_chunks(data: bytes):
    result = []
    for i in range(0, len(data), 4):
        result.append(data[i:i+4][::-1])
    return b''.join(result)
