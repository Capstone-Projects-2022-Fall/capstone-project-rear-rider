#!/usr/bin/env python3
import signal
from sys import stdout
from typing import Callable, Literal, Union

from advertisement.rear_rider_adv import RearRiderAdvertisement

from bluez.example_advertisement import LE_ADVERTISING_MANAGER_IFACE
from bluez.example_gatt_server import find_adapter, dbus, BLUEZ_SERVICE_NAME, GATT_MANAGER_IFACE
from gi.repository import GLib
from agent.simple import Agent

from services.hello_world import HelloWorldService
from services.characteristics.strobe_light import StrobeLight
from services.sensors import SensorsService

from rearrider_app import RearRiderApplication

AGENT_MANAGER_IFACE = 'org.bluez.AgentManager1'
AGENT_PATH = '/bluez/simpleagent'
BLUETOOTH_ALIAS = 'RearRiderPi4'


def main(print, on_ready: Union[None, Callable[[HelloWorldService, SensorsService], None]], on_read: Callable[[], str],
        strobe_light: StrobeLight):
    """
    """
    # First check all the variables are not none in order to ensure the main is valid.
    try:
        assert(print != None)
        assert(on_ready != None)
        assert(on_read != None)
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

    def get_object_interface(INTERFACE: Literal):
        return dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
            INTERFACE)

    adapter_props = get_object_interface('org.freedesktop.DBus.Properties')
    adapter_props.Set('org.bluez.Adapter1',
                      'Powered', dbus.Boolean(1))

    service_manager = get_object_interface(GATT_MANAGER_IFACE)

    ad_manager = get_object_interface(LE_ADVERTISING_MANAGER_IFACE)

    app = RearRiderApplication(bus, read_data=on_read,
        strobe_light=strobe_light
    )

    def register_app():

        def register_app_cb():
            print('RegisterApplication was successful.')
            adapter_props.Set("org.bluez.Adapter1", "Alias", BLUETOOTH_ALIAS)
            adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))
            adapter_props.Set("org.bluez.Adapter1", "Discoverable", dbus.Boolean(1))

        def unregister_app_cb():
            print('RegisterApplication was successful.')
            adapter_props.Set("org.bluez.Adapter1", "Alias", None)
            # adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))
            adapter_props.Set("org.bluez.Adapter1", "Discoverable", dbus.Boolean(0))

        def register_app_error_cb():
            print('RegisterApplication was unsuccessful.')

        print('Registering GATT application...')

        service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)
        
        unregister_app_cb
    

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
                on_ready(app.hello_world_service, app.sensors_service)
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
            agent_manager.UnregisterDefaultAgent(AGENT_PATH)
        
        return unregister_agent

    mainloop = GLib.MainLoop()

    unregister_app = register_app()

    unregister_agent = register_agent()

    unregister_advertisement = register_advertisement()

    mainloop.run()

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
