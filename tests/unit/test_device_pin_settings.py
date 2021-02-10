import pytest

from tests.utils.device_mock import DeviceMock

@pytest.fixture()
def device():
    dev = DeviceMock({
        0x27: bytes.fromhex('e5b4e8de36e711a9')
    })
    return dev

@pytest.fixture()
def settings(device):
    return device.pin_settings

class TestEncryptionPinSettings:
    def test_pin_enabled(self, settings):
        assert settings.pin_enabled == True

    def test_pin_number(self, settings):
        assert settings.pin_number == 4617

    def test_disable_pin(self, device):
        device.pin_settings.pin_number = 0
        device.pin_settings.pin_enabled = False
        device.pin_settings.save()

        assert device.ble_device.handlers_history.pop() == 0x27
        assert device.fields['pin_settings'].raw_data[0x27].pin_number == 0
        assert device.fields['pin_settings'].raw_data[0x27].pin_enabled == False
        assert device.ble_device.sent_data_history.pop() == bytes.fromhex('19854b04365f7f62')

    def test_enable_pin(self, device):
        device.pin_settings.pin_number = 9021
        device.pin_settings.pin_enabled = True
        device.pin_settings.save()

        assert device.ble_device.handlers_history.pop() == 0x27
        assert device.fields['pin_settings'].raw_data[0x27].pin_number == 9021
        assert device.fields['pin_settings'].raw_data[0x27].pin_enabled == True
        assert device.ble_device.sent_data_history.pop() == bytes.fromhex('e28c1ff50892b8a1')

