#!/usr/bin/env python3
from sys import stdout
from typing import Callable, Literal, Union

from rear_rider_device.rear_rider_bluetooth_server.src.advertisement.rear_rider_adv import RearRiderAdvertisement

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
    _discoverable: str
    """
    "0" or "1"
    """
    _on_discoverable_changed: Union[None, Callable[[str], None]]
    def __init__(self, bus: dbus.SystemBus, hello_world_svc: HelloWorldService, sensors_svc: SensorsService):
        self._bus = bus
        self._adapter = find_adapter(self._bus)
        get_object_interface = get_object_interface_getter(bus, self._adapter)
        self._adapter_props = get_object_interface(DBUS_PROPS_IFACE)
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
                    self.set_discoverable(str(changed.get('Discoverable')))
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
    
    def set_discoverable(self, value: str):
        if value != '0' and value != '1':
            raise Exception('discoverable value must be `0` or `1`')
        self._discoverable = value
        if self._on_discoverable_changed is not None:
            self._on_discoverable_changed(self._discoverable)
        
    def set_on_discoverable_changed(self, callback: Callable[[str], None]):
        """
        Callback should expect that value be "0" or "1"
        """
        self._on_discoverable_changed = callback
        self._on_discoverable_changed(self._discoverable)
    
    def get_discoverable_timeout(self):
        return int(self._adapter_props.Get('org.bluez.Adapter1',
                      'DiscoverableTimeout'))

    ##
    # Pairing
    ##

    def _set_pairable(self, value: bool):
        self._adapter_props.Set('org.bluez.Adapter1', 'Pairable', dbus.Boolean(value))
    
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
            # Turn off discoverability
            self.set_discoverable('0')
            self._connected_device = device
            return
        # connect == False, therefore this device was just disconnected.
        if (self._connected_device is not None and
            self._connected_device.get_address() != device.get_address()):
            # Since we only expect one device to be connected, we do not expect to reach this. 
            raise Exception(
                'Expected _connected_device to be not None and the object paths to be the same.\n'
                f'{self._connected_device.get_address()} {device.get_address()}')
        self._connected_device = None
        self._set_pairable(True)
        self.set_discoverable('1')
    
    def has_connected_device(self):
        return self._connected_device is not None
        

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
            # rear_rider_adv.Powe
            if on_ready is not None:
                rear_rider_bt = RearRiderBluetooth(bus, app.hello_world_service, app.sensors_service)
                # Get initial value
                # discoverable = '0'
                discoverable = adapter_props.Get("org.bluez.Adapter1", "Discoverable")
                rear_rider_bt.set_discoverable(str(discoverable))
                # print(f'Initial "discoverable" value: {discoverable}')
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
