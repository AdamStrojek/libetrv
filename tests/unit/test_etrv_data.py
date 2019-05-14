from datetime import datetime
from libetrv.data_struct import eTRVData, eTRVField
from libetrv.device import eTRVDeviceMeta
from libetrv.fields import UTCDateTimeField, TemperatureField


class SampleBtle:
    default_test_data = bytes.fromhex('abcdef5cdaa618ee')
    test_data = None
    handlers_history = None
    sent_data_history = None

    def __init__(self, test_data=None):
        if test_data is None:
            test_data = {}
        self.test_data = test_data
        self.handlers_history = []
        self.sent_data_history = []

    def readCharacteristic(self, handler):
        self.handlers_history.append(handler)
        return self.test_data.get(handler, self.default_test_data)

    def writeCharacteristic(self, handler, data):
        self.handlers_history.append(handler)
        self.sent_data_history.append(data)
        return True


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
    room_temp = TemperatureField(0x02, 'temp1')

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
            """,
        }
        use_encoding = False


class SampleDevice(metaclass=eTRVDeviceMeta):
    sample_data = SampleData()
    complex_data = ComplexData()

    def __init__(self, test_data=None):
        self.ble_device = SampleBtle(test_data)

    def is_connected(self):
        return True


class TestData:
    def test_init_data(self):
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
            0x02: bytes.fromhex('2c'),
        })
        assert obj.complex_data.datetime == datetime(2019, 5, 14, 11, 27, 20)
        assert obj.complex_data.room_temp == 22
        assert obj.complex_data.raw_data[0x02].temp1 == 44
