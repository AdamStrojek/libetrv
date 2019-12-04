import pytest

from tests.utils.device_mock import DeviceMock


@pytest.fixture()
def device():
    dev = DeviceMock({
        0x3f: bytes.fromhex('0123456789abcdef0123456789abcdef')
    })
    return dev


class TestEncryptionSecretKey:
    def test_read_battery(self, device):
        assert device.secret_key == '0123456789abcdef0123456789abcdef'
