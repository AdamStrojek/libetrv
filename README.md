# eTRV2MQTT

**Application is currently under development and it is not design to be used by end user**

Monitor and control your eTRV over MQTT. Recently Danfoss has released new TRVs that can be controlled
over BLE. This service will allow connect this devices directly to any Smart Home software that supports MQTT.

Application was developed on Raspberry Pi  B+

## Supported Devices

All supported and tested devices:

- Danfoss Eco Bluetooth LE

## Installation
This software requires at least Python 3.5. All required packages are listed in file `requirements.txt`.

Because software is under development there is no direct way to install it on system and setup it as system service.

For development just create virtual env and install all requirements.

```bash
$ mkdir -p ~/venv/etrv2mqtt
$ python3 -m venv ~/venv/etrv2mqtt
$ source ~/venv/etrv2mqtt/bin/activate
$ pip3 install -r requirements.txt
```
  

## Bluetooth Permissions
It is recommended to not start this app as `root` user. To avoid this you can allow python3 to access to Bluetooth interface

```bash
$ sudo apt-get install libcap2-bin
$ sudo setcap 'cap_net_raw,cap_net_admin+eip' `readlink -f \`which python3\``
$ sudo setcap 'cap_net_raw+ep' `readlink -f \`which hcitool\``
```
