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
    def test_adaptable_regulation(self, settings):
        assert settings.adaptable_regulation == True

    def test_vertical_instalation(self, settings):
        assert settings.vertical_instalation == False

    def test_display_flip(self, settings):
        assert settings.display_flip == False

    def test_slow_regulation(self, settings):
        assert settings.slow_regulation == True

    def test_valve_installed(self, settings):
        assert settings.valve_installed == True

    def test_lock_control(self, settings):
        assert settings.lock_control == False

    def test_minimum_available_temperature(self, settings):
        assert settings.temperature_min == 6.0

    def test_maximum_available_temperature(self, settings):
        assert settings.temperature_max == 28.0

    def test_frost_protection_temperature(self, settings):
        assert settings.frost_protection_temperature == 6

    def test_schedule_mode(self, settings):
        assert settings.schedule_mode == ScheduleMode.SCHEDULED
        assert settings.schedule_mode != 1

    def test_vacation_temperature(self, settings):
        assert settings.vacation_temperature == 15
