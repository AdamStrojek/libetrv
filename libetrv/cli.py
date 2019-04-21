import fire

class CLI:
    def __init__(self, pin=b'0000', secret=None):
        self._pin = pin
        self._secret = secret
        self.temperature = Temperature(pin, secret)

    def scan(timeout=10):
        pass

    def retrive_key(self, *devices):
        pass

class Temperature:
    """
    Control temperature for selected thermostat
    """

    def __init__(self, pin, secret):
        self._pin = pin
        self._secret = secret

    def get():
        """Get currently set temperature for thermostat"""
        pass
    
    def set(value):
        """Set new templerature in manual mode for thermostat"""
        pass

if __name__ == "__main__":
    fire.Fire(CLI)
