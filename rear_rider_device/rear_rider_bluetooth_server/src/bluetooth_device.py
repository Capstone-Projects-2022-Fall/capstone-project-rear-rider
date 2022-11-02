import dbus

BLUEZ_SERVICE_NAME = 'org.bluez'
BLUEZ_DEVICE_1 = 'org.bluez.Device1'
DBUS_PROPS_IFACE = 'org.freedesktop.DBus.Properties'


class BluetoothDevice:
    """
    Represents a bluetooth device.
    """
    def __init__(self, bus: dbus.Bus, device_path: str):
        self._device = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, device_path),
            DBUS_PROPS_IFACE)

    def address(self):
        return str(self._device.Get('org.bluez.Device1', 'Address'))
    
    def get_object_path(self):
        return str(self._device.object_path)
    
    def disconnect(self):
        self._device.Disconnect()
