#!/usr/bin/env python3
from bluez.example_gatt_server import find_adapter, dbus, BLUEZ_SERVICE_NAME, GATT_MANAGER_IFACE, GObject
from rearrider_app import RearRiderApplication

def main():
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    adapter = find_adapter(bus)
    if not adapter:
        print('GattManager1 interface not found')
        return

    service_manager = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, adapter),
            GATT_MANAGER_IFACE)

    app = RearRiderApplication(bus)

    mainloop = GObject.MainLoop()

    print('Registering GATT application...')

    service_manager.RegisterApplication(app.get_path(), {},
                                    reply_handler=register_app_cb,
                                    error_handler=register_app_error_cb)

    mainloop.run()

def register_app_cb():
    pass

def register_app_error_cb():
    pass

if __name__ == '__main__':
    main()