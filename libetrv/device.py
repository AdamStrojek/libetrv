from time import sleep

from bluepy import btle


class eTRVDevice(object):
    BATTERY_LEVEL_R = 0x0010

    PIN_W = 0x0024

    MANUAL_TEMPERATURE_RW = 0x002d

    SECRET_R = 0x003f

    def __init__(self, address, secret=None):
        """
        Constructor for eTRVDevice
        """
        self.address = address
        self.secret = secret
        self.pin = b'0000'
        self.ble_device = None  # type: btle.Peripheral

    def is_connected(self):
        return self.ble_device is not None

    def connect(self):
        if self.is_connected():
            return

        while True:
            try:
                self.ble_device = btle.Peripheral(self.address)
                self.__send_pin()
                break
            except btle.BTLEDisconnectError as exc:
                sleep(0.1)

    def disconnect(self):
        if self.ble_device is not None:
            self.ble_device.disconnect()

    def __send_pin(self):
        self.ble_device.writeCharacteristic(eTRVDevice.PIN_W, self.pin, True)

    def get_encryption_key(self):
        pass

    @property
    def temperature(self):
        return None

    @temperature.setter
    def set_temperature(self, value):
        pass

    @property
    def battery(self):
        if not self.is_connected():
            self.connect()

        res = self.ble_device.readCharacteristic(eTRVDevice.BATTERY_LEVEL_R)
        return res[0]
