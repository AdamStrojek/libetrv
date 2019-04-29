import pytest

from libetrv.data_struct import ScheduleStruct
from libetrv.schedule import Schedule


@pytest.fixture()
def data():
    return bytes([
        44, 37, # home, away temperature
        0, 10, 31, 48, 0, 0,  # monday
        0, 10, 31, 48, 0, 0,  # tuesday
        0, 10, 31, 48, 0, 0,  # wednesday
        0, 10, 31, 48, 0, 0,  # thursday
        0, 10, 31, 48, 0, 0,  # friday
        0, 10, 31, 48, 0, 0,  # saturday
        0, 10, 31, 48, 0, 0,  # sunday
    ])


@pytest.fixture()
def data_struct(data):
    obj = ScheduleStruct()
    obj.unpack(data)
    return obj


class TestScheduleStruct:
    def test_unpack(self, data):
        obj = ScheduleStruct()
        obj.unpack(data)
        assert obj.home_temperature == 44
        assert obj.away_temperature == 37
        assert len(obj.schedule) == 7
        for i in range(7):
            assert obj.schedule[i].data == [0, 10, 31, 48, 0, 0]


class TestScheduleParsing:
    def test_parsing(self, data_struct):
        obj = Schedule.from_struct(data_struct)
        assert obj.home_temperature == 22
        assert obj.away_temperature == 18.5
        assert len(obj.schedule) == 7
        for i in range(7):
            assert len(obj.schedule[i]) == 4
            assert obj.schedule[i][0] == (False, 0, 0)
            assert obj.schedule[i][1] == (True, 5, 0)
            assert obj.schedule[i][2] == (False, 15, 30)
            assert obj.schedule[i][3] == (True, 24, 0)
