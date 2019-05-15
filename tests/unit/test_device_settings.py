import pytest

from libetrv.data_struct import ScheduleMode

from tests.utils.device_mock import DeviceMock


@pytest.fixture()
def device():
    dev = DeviceMock({
        0x2a: bytes.fromhex('be41eca133d91760cf59ae39a5478ea2')
    })
    return dev

@pytest.fixture()
def settings(device):
    return device.settings

class TestEncryptionSettings:
    def test_frost_protection_temperature(self, settings):
        assert settings.frost_protection_temperature == 6

    def test_schedule_mode(self, settings):
        assert settings.schedule_mode == ScheduleMode.SCHEDULED
        assert settings.schedule_mode != 1

    def test_vacation_temperature(self, settings):
        assert settings.vacation_temperature == 15
