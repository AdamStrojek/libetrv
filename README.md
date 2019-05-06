# libetrv

[![CircleCI](https://circleci.com/gh/AdamStrojek/libetrv.svg?style=shield)](https://circleci.com/gh/AdamStrojek/libetrv)

**Library is currently under development and it is not design to be used by end user**

Monitor and control your eTRV from Python. Recently Danfoss has released new TRVs that can be controlled
over Bluetooth Low Energy. This library will allow connect this devices and control them.

Application was developed on a Raspberry Pi  B+, but should work fine on any Linux based system with Bluetooth LE device.

## Supported Devices

All supported and tested devices:

- Danfoss Eco Bluetooth LE - WIP

## Installation
This software requires at least Python 3.5. All required packages are listed in file `requirements.txt`.

Because software is under development there is no direct way to install it on system and setup it as system service.

For development just create virtual env and install all requirements.

```bash
$ mkdir -p ~/venv/libetrv
$ python3 -m venv ~/venv/libetrv
$ source ~/venv/libetrv/bin/activate
$ pip3 install -r requirements.txt
```
  

## Bluetooth Permissions
It is recommended to not start this app as `root` user. To avoid this you can allow python3 to access to Bluetooth interface

```bash
$ sudo apt-get install libcap2-bin
$ sudo setcap 'cap_net_raw,cap_net_admin+eip' `readlink -f \`which python3\``
$ sudo setcap 'cap_net_raw+ep' `readlink -f \`which hcitool\``
```
