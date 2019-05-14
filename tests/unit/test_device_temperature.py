import pytest
from unittest import mock

from libetrv.data_struct import ScheduleMode

from tests.utils.device_mock import DeviceMock


@pytest.fixture()
def device():
    dev = DeviceMock({
        0x2d: bytes.fromhex('8603601eaBa0f78e')
    })
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
        device.temperature.set_point_temperature = 15
        assert device.ble_device.handlers_history.pop() == 0x2d
