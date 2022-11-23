import dbus

BLUEZ_SERVICE_NAME = 'org.bluez'
BLUEZ_DEVICE_1 = 'org.bluez.Device1'
DBUS_PROPS_IFACE = 'org.freedesktop.DBus.Properties'


class BluetoothDevice:
    """
    Represents a bluetooth device.
    """
    def __init__(self, bus: dbus.Bus, device_path: str):
        self._props = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, device_path),
            DBUS_PROPS_IFACE)
        self._device = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, device_path),
            BLUEZ_DEVICE_1)

    def get_address(self):
        '''
        Return the bluetooth MAC address of this device.
        '''
        return str(self._props.Get(BLUEZ_DEVICE_1, 'Address'))

    def disconnect(self):
        '''
        Disconnect this device.
        '''
        self._device.Disconnect()

    def __str__(self) -> str:
        return (
            f'Address: {self.get_address()}'
        )
