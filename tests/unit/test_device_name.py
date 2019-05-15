import pytest

from tests.utils.device_mock import DeviceMock


@pytest.fixture()
def device():
    dev = DeviceMock({
        0x30: bytes.fromhex('318cfe8ed76f335e18f85cb8338514b3')
    })
    return dev


class TestEncryptionTemperature:
    def test_read_name(self, device):
        assert device.name == "Sample eTRV"

    def test_write_name(self, device):
        device.name = "Sample eTRV"
        assert device.fields['name'].raw_data[0x30].name == b'Sample eTRV\0\0\0\0\0'
        assert device.ble_device.handlers_history.pop() == 0x30
        assert device.ble_device.sent_data_history.pop() == bytes.fromhex('318cfe8ed76f335e18f85cb8338514b3')

        device.name = "Other eTRV"
        assert device.ble_device.handlers_history.pop() == 0x30
        assert device.ble_device.sent_data_history.pop() == bytes.fromhex('fd10eb0b2796c6c2346da16fad3bebd8')
