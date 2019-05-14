import pytest
from datetime import datetime
from libetrv.data_struct import eTRVData, eTRVField
from libetrv.device import eTRVDevice
from libetrv.fields import UTCDateTimeField, TemperatureField
from libetrv.properties import eTRVProperty

from tests.utils.device_mock import DeviceMock


class SampleData(eTRVData):
    field1 = eTRVField()
    field2 = eTRVField(read_only=True)
    field3 = UTCDateTimeField()
    field4 = eTRVField()

    class Meta:
        structure = {
            0x01: """
                unsigned char field1;
                unsigned short field2;
                unsigned int field3;
                unsigned char field4;
            """,
        }
        use_encoding = False


class ComplexData(eTRVData):
    datetime = UTCDateTimeField(0x01, 'field3')
    room_temp = TemperatureField(0x02, 'temp1', read_only=True)
    set_temp = TemperatureField(0x02)

    class Meta:
        structure = {
            0x01: """
                unsigned char field1;
                unsigned short field2;
                unsigned int field3;
                unsigned char field4;
            """,
            0x02: """
                unsigned char temp1;
                unsigned char set_temp;
            """,
        }
        use_encoding = False


class SampleDevice(DeviceMock):
    sample_data = eTRVProperty(SampleData)
    complex_data = eTRVProperty(ComplexData)

    def is_connected(self):
        return True


class TestData:
    def test_init_data(self):
        with pytest.raises(TypeError):
            obj = SampleData()

    def test_init_device(self):
        obj = SampleDevice()
        assert hasattr(obj.sample_data, 'raw_data')
        assert isinstance(obj.sample_data, eTRVData)

    def test_retrive_sample_data(self):
        obj = SampleDevice()
        assert obj.sample_data.field1 == 0xab
        assert obj.sample_data.field2 == 0xcdef
        assert obj.sample_data.field3 == datetime(2019, 5, 14, 11, 27, 20)
        assert obj.sample_data.field4 == 0xee
    
    def test_retrive_complex_data(self):
        obj = SampleDevice({
            0x01: bytes.fromhex('abcdef5cdaa618ee'),
            0x02: bytes.fromhex('2c2c'),
        })
        assert obj.complex_data.datetime == datetime(2019, 5, 14, 11, 27, 20)
        assert obj.complex_data.room_temp == 22
        assert obj.complex_data.raw_data[0x02].temp1 == 44

    def test_set_data(self):
        obj = SampleDevice({
            0x01: bytes.fromhex('abcdef5cdaa618ee'),
            0x02: bytes.fromhex('2c2c'),
        })
        with pytest.raises(AttributeError):
            obj.complex_data.room_temp = 20
        assert obj.complex_data.set_temp == 22
        obj.complex_data.set_temp = 20
        assert obj.complex_data.set_temp == 20
        assert obj.complex_data.raw_data[0x02].set_temp == 40

    def test_multiple_devices(self):
        """
        This test check does descriptors correctly save info in object
        instead of class. There should be possibility to use multiple devices
        at same time
        """
        dev_a = SampleDevice()
        dev_b = SampleDevice()
        
        assert dev_a.sample_data.field1 == 0xab
        assert dev_a.sample_data.field2 == 0xcdef
        assert dev_a.sample_data.field3 == datetime(2019, 5, 14, 11, 27, 20)
        assert dev_a.sample_data.field4 == 0xee

        assert dev_b.sample_data.field1 == 0xab
        assert dev_b.sample_data.field2 == 0xcdef
        assert dev_b.sample_data.field3 == datetime(2019, 5, 14, 11, 27, 20)
        assert dev_b.sample_data.field4 == 0xee

        dev_a.sample_data.field1 = 0xfa

        assert dev_a.sample_data.field1 == 0xfa
        assert dev_b.sample_data.field1 == 0xab
