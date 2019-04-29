import pytest

from libetrv.data_struct import ScheduleStruct
from libetrv.exceptions import ParsingError
from libetrv.schedule import Schedule


@pytest.fixture()
def data():
    return bytes([
        44, 37,  # home, away temperature
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


@pytest.fixture()
def malformed_data():
    return bytes([
        44, 37,  # home, away temperature
        0, 10, 31, 48, 0, 0,  # correct
        3, 10, 31, 48, 0, 0,  # does not start from 0
        0, 10, 31, 50, 0, 0,  # time exeeds 24h (value 48)
        0, 10, 48, 0, 0, 0,  # does not close whole cycle
        0, 10, 10, 31, 31, 48,  # duplicated entries
        0, 10, 31, 48, 0, 0,  # 
        0, 10, 31, 48, 0, 0,  # 
    ])


@pytest.fixture()
def malformed_data_struct(data):
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
    def test_parsing_correct_data(self, data_struct):
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

    def test_parsing_malformed_data_fail(self, malformed_data_struct):
        with pytest.raises(ParsingError):
            obj = Schedule.from_struct(malformed_data_struct, False)
