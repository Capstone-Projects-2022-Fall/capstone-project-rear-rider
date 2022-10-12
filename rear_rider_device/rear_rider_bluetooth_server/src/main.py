#!/usr/bin/env python3
from sys import stdout
from typing import Callable, Literal, Union

from advertisement.rear_rider_adv import RearRiderAdvertisement

from bluez.example_advertisement import LE_ADVERTISING_MANAGER_IFACE, TestAdvertisement
from bluez.example_gatt_server import find_adapter, dbus, BLUEZ_SERVICE_NAME, GATT_MANAGER_IFACE, GObject
from services.hello_world import HelloWorldService
from rearrider_app import RearRiderApplication

def main(print, on_ready: Union[None, Callable[[HelloWorldService], None]], on_read: Callable[[], str]):
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    adapter = find_adapter(bus)
    if not adapter:
        print('GattManager1 interface not found')
        return

    def get_object_interface(INTERFACE: Literal):
        return dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, adapter),
            INTERFACE)

    service_manager = get_object_interface(GATT_MANAGER_IFACE)

    ad_manager = get_object_interface(LE_ADVERTISING_MANAGER_IFACE)

    app = RearRiderApplication(bus, read_data=on_read)

    def register_app():

        def register_app_cb():
            print('RegisterApplication was successful.')
            pass

        def register_app_error_cb():
            print('RegisterApplication was unsuccessful.')
            pass

        print('Registering GATT application...')

        service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)
    

    rear_rider_adv = RearRiderAdvertisement(bus, 0)

    def register_advertisement():
        """
        Returns the unregister_advertisement function.
        """
        timeout = 0
        def register_ad_cb():
            print('Advertisement registered')
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

    mainloop = GObject.MainLoop()

    register_app()

    unregister_advertisement = register_advertisement()

    mainloop.run()

    unregister_advertisement()


if __name__ == '__main__':
    main(print, None, None)