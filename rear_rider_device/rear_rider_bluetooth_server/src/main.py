#!/usr/bin/env python3
from sys import stdout
from typing import Callable, Literal, Union

from rear_rider_device.rear_rider_bluetooth_server.src.advertisement.rear_rider_adv import RearRiderAdvertisement
from rear_rider_device.rear_rider_bluetooth_server.src.bluetooth_adapter import BluetoothAdapter

from rear_rider_device.rear_rider_bluetooth_server.src.bluez.example_advertisement import LE_ADVERTISING_MANAGER_IFACE
from rear_rider_device.rear_rider_bluetooth_server.src.bluez.example_gatt_server import find_adapter, dbus, BLUEZ_SERVICE_NAME, GATT_MANAGER_IFACE
from gi.repository import GLib
from rear_rider_device.rear_rider_bluetooth_server.src.agent.simple import Agent
from rear_rider_device.rear_rider_bluetooth_server.src.bluetooth_device import BluetoothDevice

from rear_rider_device.rear_rider_bluetooth_server.src.services.hello_world import HelloWorldService
from rear_rider_device.rear_rider_bluetooth_server.src.services.characteristics.strobe_light import StrobeLight
from rear_rider_device.rear_rider_bluetooth_server.src.services.sensors import SensorsService

from rear_rider_device.rear_rider_bluetooth_server.src.rearrider_app import RearRiderApplication

AGENT_MANAGER_IFACE = 'org.bluez.AgentManager1'
AGENT_PATH = '/bluez/simpleagent'
BLUETOOTH_ALIAS = 'RearRiderPi4'
BLUEZ_DEVICE_1 = 'org.bluez.Device1'
DBUS_PROPS_IFACE = 'org.freedesktop.DBus.Properties'
DISCOVERABLE = 1
"""
0 = False
1 = True
"""
DISCOVERABLE_TIMEOUT = 0
"""
0 timeout means the device will stay in discoverable mode.
Ideally we should have the timeout be some finite duration, but we do not
have any way to turn the discovery back on after it times out. If we add a
push button to the device, we can have that trigger discovery mode.
"""

def get_object_interface_getter(bus: dbus.Bus, adapter):
    def get_object_interface(INTERFACE: Literal):
        return dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
            INTERFACE)
    return get_object_interface

class RearRiderBluetooth:
    _discoverable: bool
    _on_discoverable_changed: Union[None, Callable[[bool], None]]
    def __init__(self, bus: dbus.SystemBus, hello_world_svc: HelloWorldService, sensors_svc: SensorsService):
        self._bus = bus
        self._adapter = BluetoothAdapter(bus)
        self._connected_device: Union[None, BluetoothDevice] = None
        self.hello_world_svc = hello_world_svc
        self.sensors_svc = sensors_svc
        self._on_discoverable_changed = None

        # Set up listening to bluetooth property changes such as discoverability.
        def listen_to_bluetooth_property_changes():
            def bt_properties_changed(interface, changed, invalidated, path):
                """
                Reference: https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/test/monitor-bluetooth
                """
                changed_props = changed.keys()
                if 'Discoverable' in changed_props:
                    self.__set_discoverable_state(bool(changed.get('Discoverable')))
                if 'Connected' in changed_props:
                    self._on_device_connection_change(
                        bool(changed.get('Connected')),
                        device_path=str(path)
                    )
            self._bus.add_signal_receiver(bt_properties_changed, bus_name="org.bluez",
                dbus_interface="org.freedesktop.DBus.Properties",
                signal_name="PropertiesChanged",
                path_keyword="path")
        listen_to_bluetooth_property_changes()

    ##
    # Discovery
    ##
    def sync_discoverable_state(self):
        '''
        Synchronize the discoverable state by checking with the adapter properties.
        '''
        self.__set_discoverable_state(self._adapter.get_discoverable())

    def __set_discoverable_state(self, value: bool):
        '''
        Update the discoverability state.

        Calls the callback function set by `self.set_on_discoverable_changed(...)`. Takes into
        account that no device is connected.
        '''
        self._discoverable = value and self.allowing_connections()
        if self._on_discoverable_changed is not None:
            self._on_discoverable_changed(self._discoverable)

    def set_on_discoverable_changed(self, callback: Callable[[bool], None]):
        """
        Callback should expect that value be "0" or "1"
        """
        self._on_discoverable_changed = callback
        self._on_discoverable_changed(self._discoverable)

    def get_discoverable_timeout(self):
        return self._adapter.get_discoverable_timeout()

    ##
    # Pairing
    ##

    def _set_pairable(self, value: bool):
        self._adapter.set_pairable(value)

    def _on_device_connection_change(self, connected: bool, device_path: str):
        device = BluetoothDevice(self._bus, device_path)
        if connected:
            if self._connected_device is not None:
                if device.get_address() == self._connected_device.get_address():
                    return
                device.disconnect()
                raise Exception('We only want one device at a time to be connected.')
            # Disable pairing since we only want one device at a time to be connected.
            self._set_pairable(False)
            self._connected_device = device
            self.sync_discoverable_state()
            return
        # connect == False, therefore this device was just disconnected.
        if (self._connected_device is not None and
            self._connected_device.get_address() != device.get_address()):
            # Since we only expect one device to be connected, we do not expect to reach this. 
            raise Exception(
                'Expected _connected_device to be not None and the object paths to be the same.\n'
                f'{self._connected_device.get_address()} {device.get_address()}')
        self._connected_device = None
        self.__remove_devices(self._adapter.get_device_list())
        self._set_pairable(True)
        self.sync_discoverable_state()

    def __remove_devices(self, devices: list[BluetoothDevice]):
        for device in devices:
            self._adapter.remove_device(device)

    def allowing_connections(self):
        '''
        Returns true or false denoting if new device connections are allowed.
        '''
        return self._connected_device is None

    def kick_and_remove_devices_if_not_alone(self):
        '''
        Remove/Forget all paired devices under the following conditions:

        - Not currently connected.
        - Is connected, but is also not the only connected devices.

        This effectively ensures at most one device is connected, and implements a work around for
        having to manually "remove" a device via `bluetoothctl`.
        '''
        devices = self._adapter.get_device_list(only_if_paired=True)
        connected_devices: list[BluetoothDevice] = []
        disconnected_devices: list[BluetoothDevice] = []
        for device in devices:
            if device.connected():
                connected_devices.append(device)
                continue
            disconnected_devices.append(device)

        len_connected_devices = len(connected_devices)
        if len_connected_devices == 1:
            # connected
            self._connected_device = connected_devices[0]
        else:
            # connected devices are 0: skip for ... in ...:
            for connected_device in connected_devices:
                # connected devices are > 1
                connected_device.disconnect()
                disconnected_devices.append(connected_device)
        self.__remove_devices(disconnected_devices)
        
def main(print, on_ready: Union[None, Callable[[RearRiderBluetooth], None]], strobe_light: StrobeLight):
    """
    """
    # First check all the variables are not none in order to ensure the main is valid.
    try:
        assert(print != None)
        assert(on_ready != None)
        assert(strobe_light != None)
    except AssertionError:
        print('Condition for main function not met!')
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    adapter = find_adapter(bus)
    if not adapter:
        print('GattManager1 interface not found')
        return

    get_object_interface = get_object_interface_getter(bus, adapter)

    adapter_props = get_object_interface(DBUS_PROPS_IFACE)
    adapter_props.Set('org.bluez.Adapter1',
                      'Powered', dbus.Boolean(1))

    service_manager = get_object_interface(GATT_MANAGER_IFACE)

    ad_manager = get_object_interface(LE_ADVERTISING_MANAGER_IFACE)

    app = RearRiderApplication(bus,
        strobe_light=strobe_light
    )

    def register_app():

        def register_app_cb():
            print('RegisterApplication was successful.')
            adapter_props.Set("org.bluez.Adapter1", "Alias", BLUETOOTH_ALIAS)
            adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))
            adapter_props.Set("org.bluez.Adapter1", "Discoverable", dbus.Boolean(DISCOVERABLE))
            adapter_props.Set("org.bluez.Adapter1", "DiscoverableTimeout", dbus.UInt32(DISCOVERABLE_TIMEOUT))

        def unregister_app_cb():
            adapter_props.Set("org.bluez.Adapter1", "Alias", '')
            # adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))
            adapter_props.Set("org.bluez.Adapter1", "Discoverable", dbus.Boolean(0))

        def register_app_error_cb():
            print('RegisterApplication was unsuccessful.')

        print('Registering GATT application...')

        service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)
        
        return unregister_app_cb
    

    rear_rider_adv = RearRiderAdvertisement(bus, 0)

    def register_advertisement():
        """
        Returns the unregister_advertisement function.
        """
        timeout = 0
        def register_ad_cb():
            print('Advertisement registered')
            print(rear_rider_adv.get_properties())
            if on_ready is not None:
                rear_rider_bt = RearRiderBluetooth(bus, app.hello_world_service, app.sensors_service)
                rear_rider_bt.kick_and_remove_devices_if_not_alone()
                rear_rider_bt.sync_discoverable_state()
                on_ready(rear_rider_bt)
            else:
                stdout.write('ready\n')
                stdout.flush()

        def register_ad_error_cb(error):
            print('Failed to register advertisement: ' + str(error))
            mainloop.quit()

        def unregister_advertisement():
            ad_manager.UnregisterAdvertisement(rear_rider_adv)
            print('Advertisement unregistered')
            dbus.service.Object.remove_from_connection(rear_rider_adv)
        
        ad_manager.RegisterAdvertisement(rear_rider_adv.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)

        if timeout > 0:
            # threading.Thread(target=shutdown, args=(timeout,)).start()
            pass
        else:
            print('Advertising forever...')
        
        return unregister_advertisement
    
    simple_agent = Agent(bus, AGENT_PATH)
    def register_agent():
        obj = bus.get_object(BLUEZ_SERVICE_NAME, '/org/bluez')
        agent_manager = dbus.Interface(obj, AGENT_MANAGER_IFACE)
        agent_manager.RegisterAgent(AGENT_PATH, 'NoInputNoOutput')
        agent_manager.RequestDefaultAgent(AGENT_PATH)

        def unregister_agent():
            agent_manager.UnregisterAgent(AGENT_PATH)
        
        return unregister_agent

    mainloop = GLib.MainLoop()

    unregister_app = register_app()

    unregister_agent = register_agent()

    unregister_advertisement = register_advertisement()

    try:
        mainloop.run()
    finally:
        unregister_advertisement()

        unregister_agent()

        unregister_app()



if __name__ == '__main__':
    # This main function is used only for testing purposes.

    strobe_on = False

    def turn_on():
        """
        Tests turning on the strobe light.
        """
        strobe_on = True
        print("on")
    
    def turn_off():
        """
        Tests turning off the strobe light.
        """
        strobe_on = False
        print("off")
    
    def is_on():
        """
        Tests turning on the strobe light.
        """
        return strobe_on

    strobe_light = StrobeLight(
        turn_on,
        turn_off,
        is_on,
        frequency=5
    )
    main(print, None, None, strobe_light)
