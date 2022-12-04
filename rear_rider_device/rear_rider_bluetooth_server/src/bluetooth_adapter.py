from typing import TypeVar
import dbus
from rear_rider_device.rear_rider_bluetooth_server.src.bluez.example_gatt_server import find_adapter
from rear_rider_device.rear_rider_bluetooth_server.src.bluetooth_device import BluetoothDevice

BLUEZ_SERVICE_NAME = 'org.bluez'
DBUS_PROPS_IFACE = 'org.freedesktop.DBus.Properties'
OBJECT_MANAGER_IFACE = 'org.freedesktop.DBus.ObjectManager'
ADAPTER_IFACE = 'org.bluez.Adapter1'
DEVICE_IFACE = 'org.bluez.Device1'

class BluetoothAdapter:
    '''
    Reference:
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/adapter-api.txt
    '''
    def __init__(self, bus: dbus.SystemBus):
        self._bus = bus
        self._adapter_path = _find_adapter(bus)
        self._adapter = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, self._adapter_path),
            ADAPTER_IFACE)
        self._adapter_props = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, self._adapter_path),
            DBUS_PROPS_IFACE)
        self._manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
            OBJECT_MANAGER_IFACE)

    def __adapter_get(self, prop: str):
        '''
        prop
            This is the name of the property as defined by the bluez docs.
        '''
        return self._adapter_props.Get(ADAPTER_IFACE, prop) 

    def __adapter_set(self, prop: str, value):
        '''
        prop
            This is the name of the property as defined by the bluez docs.
        value
            The property named `prop` is set to this value. The value must be one of the dbus types.
        '''
        return self._adapter_props.Set(ADAPTER_IFACE, prop, value)
    
    def get_device_list(self, only_if_paired = False):
        '''
        Get the Bluetooth devices managed by this adapter.
        '''
        objects = self._manager.GetManagedObjects()
        all_devices = (str(path) for path, interfaces in objects.items() if
                            DEVICE_IFACE in interfaces.keys())
        device_list = [BluetoothDevice(self._bus, d)
            for d in all_devices if d.startswith(self.get_adapter_path() + '/')]
        if only_if_paired:
            paired_device_list = [pd for pd in device_list if pd.paired()]
        return device_list

    def get_adapter_path(self):
        return str(self._adapter_path)
    
    def get_discoverable(self):
        return bool(self.__adapter_get('Discoverable'))

    def get_discoverable_timeout(self):
        return int(self.__adapter_get('DiscoverableTimeout'))
    
    def set_pairable(self, value: bool):
        self.__adapter_set('Pairable', dbus.Boolean(value))
    
    def remove_device(self, device: BluetoothDevice):
        self._adapter.RemoveDevice(device.get_path())

def _find_adapter(bus: dbus.SystemBus) -> dbus.ObjectPath:
    adapter = find_adapter(bus)
    if adapter is None:
        raise Exception('Expected the adapter to not be None.')
    return adapter
