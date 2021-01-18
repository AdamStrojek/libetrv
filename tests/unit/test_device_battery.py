import pytest

from tests.utils.device_mock import DeviceMock


@pytest.fixture()
def device():
    dev = DeviceMock({
        0x10: bytes.fromhex('59')
    })
    return dev


class TestEncryptionTemperature:
    def test_read_battery(self, device):
        assert device.battery == 89

    def test_write_battery(self, device):
        with pytest.raises(AttributeError):
            device.battery = 50
