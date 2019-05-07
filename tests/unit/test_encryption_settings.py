import pytest

from libetrv.data_struct import ScheduleMode
from libetrv.device import eTRVDevice

secret_key = 'df5b7d6a1632cca479306eb378b6e959'

settings_value = 'be41eca133d91760cf59ae39a5478ea2'


class PeripheralMock:
    def readCharacteristic(self, handler):
        return bytes.fromhex(settings_value)


@pytest.fixture()
def device():
    dev = eTRVDevice("00:11:22:33:44:55", secret=bytes.fromhex(secret_key))
    dev.is_connected = lambda: True
    dev.ble_device = PeripheralMock()
    return dev

@pytest.fixture()
def settings(device):
    return device.settings

class TestEncryptionSettings:
    def test_frost_protection_temperature(self, settings):
        assert settings.frost_protection_temperature == 6

    def test_schedule_mode(self, settings):
        assert settings.schedule_mode == ScheduleMode.SCHEDULED

    def test_vacation_temperature(self, settings):
        assert settings.vacation_temperature == 15
