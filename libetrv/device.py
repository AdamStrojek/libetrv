import struct
import cstruct
import enum
from time import sleep
from datetime import datetime

from bluepy import btle
from loguru import logger

from .utils import etrv_read, etrv_repack, etrv_decode, etrv_reverse_chunks


class ScheduleMode(enum.IntEnum):
    MANUAL = 0
    SCHEDULED = 1
    VACATION = 2


class SettingsStruct(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ = """
        unsigned char unknow1[3];
        unsigned char frost_protection_temperature;
        unsigned char schedule_mode;
        unsigned char vacation_temperature; 
        int vacation_from;
        int vacation_to;
        unsigned char unknow2[2];
    """


class TemperatureStruct(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ = """
        unsigned char set_point_temperature;
        unsigned char room_temperature;
        unsigned char padding[6];
    """


class TimeStruct(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ = """
        int time_local;
        int time_offset;
    """


class BatteryStruct(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ = """
        unsigned char battery;
    """


class eTRVDevice(object):
    BATTERY_LEVEL_R = 0x0010

    PIN_W = 0x0024

    TEMPERATURE_RW = 0x002d

    DEVICE_NAME_RW = 0x0030

    TIME_RW = 0x0036

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

    def connect(self, send_pin: bool = True):
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
                    self.send_pin()
                break
            except btle.BTLEDisconnectError:
                logger.error("Unable connect to {}. Retrying in 100ms", self.address)
                sleep(0.1)

    def disconnect(self):
        logger.debug("Disconnecting")
        if self.ble_device is not None:
            self.ble_device.disconnect()
            self.ble_device = None

    def send_pin(self):
        logger.debug("Write PIN to {}", self.address)
        self.ble_device.writeCharacteristic(eTRVDevice.PIN_W, self.pin, True)

    @property
    def pin(self):
        """The pin property."""
        return self._pin

    @pin.setter
    def pin(self, value):
        self._pin = value

    @etrv_read(TIME_RW, True)
    def retrieve_secret_key(self, data):
        return data.hex()

    @property
    def secret(self):
        """The secret property."""
        return self._secret
    @secret.setter
    def secret(self, value):
        self._secret = value

    @property
    @etrv_read(TEMPERATURE_RW, True, TemperatureStruct)
    def temperature(self, data: TemperatureStruct):
        """
        This property will return both current and set point temperature
        """
        room_temp = data.room_temperature * .5
        set_temp = data.set_point_temperature * .5
        return room_temp, set_temp

    @property
    def room_temperature(self):
        """
        This property will return current temperature measured on device with precision up to 0.5 degrees
        """
        room_temp, _ = self.temperature
        return room_temp

    @property
    def set_point_temperature(self):
        """
        This property is responsible for set point temperature. It will allow you to not only retrieve
        current value, but also set new. Temperature will be always rounded to 0.5 degree
        """
        _, set_temp = self.temperature
        return set_temp

    @property
    @etrv_read(BATTERY_LEVEL_R, True, BatteryStruct)
    def battery(self, data: BatteryStruct):
        """
        This property will return current battery level in integer
        """
        return data.battery

    @property
    @etrv_read(DEVICE_NAME_RW, True)
    def device_name(self, data: bytes):
        # TODO This function do not work properly, need to fix later
        data = data.strip(b'\0')
        return data.decode('ascii')

    @property
    @etrv_read(TIME_RW, True, TimeStruct)
    def time(self, data: TimeStruct):
        return datetime.utcfromtimestamp(data.time_local-data.time_offset)
