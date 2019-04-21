from time import sleep

import xxtea
from bluepy import btle
from loguru import logger


class eTRVDevice(object):
    BATTERY_LEVEL_R = 0x0010

    PIN_W = 0x0024

    MANUAL_TEMPERATURE_RW = 0x002d

    SECRET_R = 0x003f

    def __init__(self, address, secret=None, pin=None):
        """
        Constructor for eTRVDevice
        """
        self.address = address
        self.secret = secret
        self.pin = b'0000' if pin is None else pin
        self.ble_device = None 
    
    @staticmethod
    def scan(timeout=10.0):
        devices = btle.Scanner().scan(timeout)

        for dev in devices:
            scan_data = dev.getScanData()
            for (adtype, desc, value) in scan_data:
                if adtype == 9 and value.endswith(';eTRV'):
                    yield dev

    def is_connected(self):
        return self.ble_device is not None

    def connect(self, send_pin=True):
        """
        This method allow you to connect to eTRV device and if it is required it will
        also send pin. You can select is it necessery
        """
        logger.debug("Trying connect to {}", self.address)
        if self.is_connected():
            logger.debug("Device already connected {}", self.address)
            return

        while True:
            try:
                self.ble_device = btle.Peripheral(self.address)
                if send_pin:
                    self.__send_pin()
                break
            except btle.BTLEDisconnectError:
                logger.error("Unable connect to {}. Retrying in 100ms", self.address)
                sleep(0.1)

    def disconnect(self):
        logger.debug("Disconnecting")
        if self.ble_device is not None:
            self.ble_device.disconnect()
            self.ble_device = None

    def __send_pin(self):
        logger.debug("Write PIN to {}", self.address)
        self.ble_device.writeCharacteristic(eTRVDevice.PIN_W, self.pin, True)

    def __write(self, service: int, data: bytes):
        if not self.is_connected():
            self.connect()

        data = data[::-1]
        res = self.ble_device.writeCharacteristic(service, data, True)  # type: bytes
        return res[::-1]

    def __read(self, service: int, send_pin: bool = True, decrypt: bool = True):
        if not self.is_connected():
            self.connect(send_pin)

        res = self.ble_device.readCharacteristic(service)  # type: bytes
        if decrypt:
            res = res[::-1]  # Change big endian to little endian
            res = xxtea.decrypt(res, self.secret, padding=False,rounds=32)

        return res

    @property
    def pin(self):
        """The pin property."""
        return self._pin

    @pin.setter
    def pin(self, value):
        self._pin = value

    def retrieve_secret_key(self):
        return self.__read(eTRVDevice.SECRET_R, False, False)

    @property
    def secret(self):
        """The secret property."""
        return self._secret
    @secret.setter
    def secret(self, value):
        self._secret = value

    @property
    def temperature(self):
        return self.__read(eTRVDevice.MANUAL_TEMPERATURE_RW)

    @temperature.setter
    def set_temperature(self, value):
        pass

    @property
    def battery(self):
        if not self.is_connected():
            self.connect()

        res = self.__read(eTRVDevice.BATTERY_LEVEL_R, True, False)
        return int(res[0])
