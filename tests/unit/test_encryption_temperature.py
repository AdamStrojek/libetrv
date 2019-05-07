import pytest
from unittest import mock

from libetrv.data_struct import ScheduleMode
from libetrv.device import eTRVDevice

secret_key = 'df5b7d6a1632cca479306eb378b6e959'

temperature_value = '8603601eaBa0f78e'


class PeripheralMock:
    def readCharacteristic(self, handler):
        return bytes.fromhex(temperature_value)


@pytest.fixture()
def device():
    dev = eTRVDevice("00:11:22:33:44:55", secret=bytes.fromhex(secret_key))
    dev.is_connected = lambda: True
    dev.ble_device = PeripheralMock()
    return dev

@pytest.fixture()
def temperature(device):
    return device.temperature


class TestEncryptionTemperature:
    def test_room_temperature(self, temperature):
        assert temperature.room_temperature == 23

    def test_set_point_temperature(self, temperature):
        assert temperature.set_point_temperature == 23

    def test_change_set_point_temperature(self, device):
        device.ble_device.writeCharacteristic = mock.Mock(return_value=True)
        temperature.set_point_temperature = 15
        assert device.ble_device.writeCharacteristic.call_count == 1
