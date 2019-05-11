from loguru import logger

try:
    from bluepy.btle import Scanner, Peripheral, BTLEDisconnectError
except ImportError:
    logger.error("Cannot import bluepy, if you are on final machine please check does everything has been installed correctly")

    class Scanner:
        def scan(self, *args, **kwargs):
            return []

    class Peripheral:
        def __init__(self, *args, **kwargs):
            pass

        def connect(self, *args, **kwargs):
            return True

        def disconnect(self, *args, **kwargs):
            return True

        def writeCharacteristic(self, *args, **kwargs):
            return True

        def readCharacteristic(self, *args, **kwargs):
            return True

    class BTLEDisconnectError(Exception):
        pass
