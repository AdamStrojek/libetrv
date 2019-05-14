from libetrv.device import eTRVDevice

class BtleMock:
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


class DeviceMock(eTRVDevice):
    def __init__(self, test_data=None):
        super().__init__('aa:bb:cc:dd:ee:ff')
        self.ble_device = BtleMock(test_data)
        self.secret = bytes.fromhex('df5b7d6a1632cca479306eb378b6e959')

    def is_connected(self):
        return True
