import time
import fire
from libetrv.device import eTRVDevice

class CLI:
    def __init__(self, pin=b'0000', secret=None):
        self._pin = pin
        if secret is not None:
            self._secret = bytes.fromhex(secret)
        else:
            self._secret = None

    def scan(self, timeout=10.):
        print("Detected eTRV devices:")
        for device in eTRVDevice.scan(timeout):
            print("{}, RSSI={}dB".format(device.addr, device.rssi))
    
    def device(self, device_id):
        return Device(device_id, self._pin, self._secret)


class Device:
    def __init__(self, device, pin, secret):
        self._pin = pin
        self._secret = secret
        self._device = eTRVDevice(device, pin=self._pin, secret=self._secret)

    def retrive_key(self):
        print(
            "In 5 seconds this script will try to retrieve a secure key from eTRV device. "
            "Don't forget to save it for later. Before that be sure that device is in pairing mode. "
            "You can achieve that by pressing button on device"
        )
        time.sleep(5)
        print("Secret Key:", self._device.retrieve_secret_key())

    def battery(self):
        battery = self._device.battery
        print("Battery level: {}%".format(battery))

class Temperature:
    """
    Control temperature for selected thermostat
    """

    def __init__(self, pin, secret):
        self._pin = pin
        self._secret = secret

    def get(self):
        """Get currently set temperature for thermostat"""
        pass
    
    def set(self, value):
        """Set new templerature in manual mode for thermostat"""
        pass

if __name__ == "__main__":
    fire.Fire(CLI)
