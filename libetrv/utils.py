from functools import wraps

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
