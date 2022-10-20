## Prerequisites
Run the command to install the relevant python packages necessary for communicating with the bluetooth daemon.

- `sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 libglib2.0-dev`

- `pip install dbus-python`
- `pip install pycairo`
- `pip install PyGObject`

## LEDs Process - leds_proc.py

Run this under sudo to give python access to the gpio in /dev/mem

```bash
sudo python ./leds_proc.py
```

## Notes

[`./bluez/example_gatt_server.py`](./bluez/example_gatt_server.py) is borrowed from https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/test/example-gatt-server