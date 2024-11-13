from collections import namedtuple
from time import sleep
from datetime import datetime

from .bluetooth import btle
from loguru import logger

from .data_struct import BatteryData, PinSettingsData, SettingsData, TemperatureData, CurrentTimeData, SecretKeyData, NameData
from .properties import eTRVProperty
from .utils import etrv_read, etrv_write


class eTRVDeviceMeta(type):
    def __new__(mcls, name, bases, attrs):
        cls = super(eTRVDeviceMeta, mcls).__new__(mcls, name, bases, attrs)
        for attr, obj in attrs.items():
            if isinstance(obj, eTRVProperty):
                obj.__set_name__(cls, attr)
        return cls


class eTRVDevice(metaclass=eTRVDeviceMeta):
    def __init__(self, address, secret=None, pin=None, retry_limit=None):
        """
        Constructor for eTRVDevice
        """
        self.address = address
        self.secret = secret
        self.pin = b'\0\0\0\0' if pin is None else pin.to_bytes(4, byteorder='big')
        self.ble_device = None 
        self.__pin_already_sent = False

        self.fields = {}
        self.retry_limit=retry_limit

    @staticmethod
    def scan(timeout=10.0, n_expected=1000):
        seen = set()
        n = 0
        for i in range(int(timeout)):
            devices = btle.Scanner().scan(2)
            for d in devices:
                if d.addr in seen:
                    continue

                seen.add(d.addr)

                scan_data = d.getScanData()

                for (adtype, desc, value) in scan_data:
                    if adtype != 9 or not value.endswith(';eTRV'):
                        continue

                    n += 1

                    # The advertisement data contains
                    # [Flags][MAC addr][Device type]
                    # If bit 2 of Flags is set then device is
                    # in setup mode and we can read the secret key
                    secret_key = None
                    flags = int(value[0])
                    if flags & 0x4:
                        eTRV = eTRVDevice(d.addr)
                        secret_key = eTRV.secret_key
                        eTRV.disconnect()

                    yield d, secret_key
                    break

            if n == n_expected:
                break

    def is_connected(self):
        return self.ble_device is not None

    def connect(self, send_pin: bool = True):
        """
        This method allow you to connect to eTRV device and if it is required it will
        also send pin. You can select is it necessery
        """
        logger.debug("Trying connect to {}", self.address)
        if self.is_connected():
            logger.debug("Device already connected {}", self.address)
            return

        retry_limit=self.retry_limit

        while retry_limit == None or retry_limit>=0:
            try:
                self.ble_device = btle.Peripheral(self.address)
                if send_pin:
                    self.send_pin()
                break
            except btle.BTLEDisconnectError:
                logger.error("Unable connect to {}. Retrying in 100ms", self.address)
                if retry_limit != None:
                    retry_limit-=1
                    if retry_limit<0:
                        raise
                sleep(0.1)

    def disconnect(self):
        logger.debug("Disconnecting")
        if self.ble_device is not None:
            self.ble_device.disconnect()
            self.ble_device = None
            self.__pin_already_sent = False
            for field in self.fields.values():
                field.invalidate()


    def send_pin(self):
        if not self.__pin_already_sent:
            logger.debug("Write PIN to {}", self.address)
            pin_handler = 0x24
            self.ble_device.writeCharacteristic(pin_handler, self.pin, True)
            self.__pin_already_sent = True

    battery = eTRVProperty(BatteryData)
    
    pin_settings = eTRVProperty(PinSettingsData)

    settings = eTRVProperty(SettingsData)

    temperature = eTRVProperty(TemperatureData)

    name = eTRVProperty(NameData)

    current_time = eTRVProperty(CurrentTimeData)

    secret_key = eTRVProperty(SecretKeyData)

    # @property
    # @etrv_read(SCHEDULE_RW, True)
    # def schedule(self, data: ScheduleStruct) -> Schedule:
    #     s = Schedule()
    #     s.parse_struct(data)
    #     return s
    # "1002000D-2749-0001-0000-00805F9B042F", "1002000E-2749-0001-0000-00805F9B042F", "1002000F-2749-0001-0000-00805F9B042F"
