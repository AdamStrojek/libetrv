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

    def get_handler(self, uuid):
        self._device.connect(False)
        ch = self._device.ble_device.getCharacteristics(uuid=uuid)[0]
        print("Handler: 0x{:02X}".format(ch.getHandle()))

    def retrive_key(self):
        print(
            "In 5 seconds this script will try to retrieve a secure key from eTRV device. "
            "Don't forget to save it for later. Before that be sure that device is in pairing mode. "
            "You can achieve that by pressing button on device"
        )
        time.sleep(5)
        print("Secret Key:", self._device.retrieve_secret_key())

    def battery(self):
        result = self._device.battery
        print("Battery level: {}%".format(result))

    def settings(self):
        result = self._device.settings
        print('Frost protection temperature: {:.1f}°C'.format(result.frost_protection_temperature))
        print('Schedule mode: {}'.format(result.schedule_mode))
        print('Vacation temperature: {:.1f}°C'.format(result.vacation_temperature))
        print('Vacation From: {}'.format(result.vacation_from.isoformat()))
        print('Vacation To: {}'.format(result.vacation_to.isoformat()))

    def temperature(self):
        temp = self._device.temperature
        print("Current temperature: {:.1f}°C".format(temp.room_temperature))
        print("Set point temperature: {:.1f}°C".format(temp.set_point_temperature))

    def name(self):
        device_name = self._device.device_name
        print("Device name: '{}'".format(device_name))

    def current_time(self):
        time_utc = self._device.current_time
        print("Current time: {}".format(time.strftime('%Y-%m-%d %H:%M:%S %Z')))


if __name__ == "__main__":
    fire.Fire(CLI)
