import sys
from libetrv.device import eTRVDevice

ETRV_ADDRESS = sys.argv[1]
if len(sys.argv) > 2:
    SECRET_KEY = bytes.fromhex(sys.argv[2])
else:
    SECRET_KEY = b''

print("Connecting to device")
dev = eTRVDevice(ETRV_ADDRESS)

print("Retrieve battery level")

print("Battery Level", dev.battery)
