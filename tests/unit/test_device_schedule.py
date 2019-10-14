import pytest

from tests.utils.device_mock import DeviceMock

from libetrv.data_struct import ScheduleData

@pytest.fixture()
def device():
    dev = DeviceMock({
        0x45: bytes.fromhex('745703b8789c1dc5049f81bf33b3a492e0fc436c'),
        0x48: bytes.fromhex('745703b8789c1dc5049f81bf'),
        0x4b: bytes.fromhex('745703b8789c1dc5049f81bf'),
    })
    return dev


class TestEncryptionSchedule:
    def test_room_and_away_temperature(self, device):
        assert 23 == device.schedule.home_temperature
        assert 19 == device.schedule.away_temperature
