#!/usr/bin/python
# SPDX-License-Identifier: LGPL-2.1-or-later

import argparse
import dbus
import dbus.mainloop.glib
import dbus.service
import json
import time

from threading import Thread

try:
    from gi.repository import GObject  # python3
except ImportError:
    import gobject as GObject  # python2

DBUS_OM_IFACE = 'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE = 'org.freedesktop.DBus.Properties'

BLUEZ_SERVICE_NAME = 'org.bluez'

ADV_MONITOR_MANAGER_IFACE = 'org.bluez.AdvertisementMonitorManager1'
ADV_MONITOR_IFACE = 'org.bluez.AdvertisementMonitor1'
ADV_MONITOR_APP_BASE_PATH = '/org/bluez/example/adv_monitor_app'


class AdvMonitor(dbus.service.Object):

    # Indexes of the Monitor object parameters in a monitor data list.
    MONITOR_TYPE = 0
    RSSI_FILTER = 1
    PATTERNS = 2

    # Indexes of the RSSI filter parameters in a monitor data list.
    RSSI_H_THRESH = 0
    RSSI_H_TIMEOUT = 1
    RSSI_L_THRESH = 2
    RSSI_L_TIMEOUT = 3

    # Indexes of the Patterns filter parameters in a monitor data list.
    PATTERN_START_POS = 0
    PATTERN_AD_TYPE = 1
    PATTERN_DATA = 2

    def __init__(self, bus, app_path, monitor_id, monitor_data):
        self.path = app_path + '/monitor' + str(monitor_id)
        self.bus = bus

        self._set_type(monitor_data[self.MONITOR_TYPE])
        self._set_rssi(monitor_data[self.RSSI_FILTER])
        self._set_patterns(monitor_data[self.PATTERNS])

        super(AdvMonitor, self).__init__(self.bus, self.path)


    def get_path(self):
        return dbus.ObjectPath(self.path)


    def get_properties(self):
        properties = dict()
        properties['Type'] = dbus.String(self.monitor_type)
        properties['RSSIHighThreshold'] = dbus.Int16(self.rssi_h_thresh)
        properties['RSSIHighTimeout'] = dbus.UInt16(self.rssi_h_timeout)
        properties['RSSILowThreshold'] = dbus.Int16(self.rssi_l_thresh)
        properties['RSSILowTimeout'] = dbus.UInt16(self.rssi_l_timeout)
        properties['Patterns'] = dbus.Array(self.patterns, signature='(yyay)')
        return {ADV_MONITOR_IFACE: properties}


    def _set_type(self, monitor_type):
        self.monitor_type = monitor_type


    def _set_rssi(self, rssi):
        self.rssi_h_thresh = rssi[self.RSSI_H_THRESH]
        self.rssi_h_timeout = rssi[self.RSSI_H_TIMEOUT]
        self.rssi_l_thresh = rssi[self.RSSI_L_THRESH]
        self.rssi_l_timeout = rssi[self.RSSI_L_TIMEOUT]


    def _set_patterns(self, patterns):
        self.patterns = []
        for pattern in patterns:
            start_pos = dbus.Byte(pattern[self.PATTERN_START_POS])
            ad_type = dbus.Byte(pattern[self.PATTERN_AD_TYPE])
            ad_data = []
            for byte in pattern[self.PATTERN_DATA]:
                ad_data.append(dbus.Byte(byte))
            adv_pattern = dbus.Struct((start_pos, ad_type, ad_data),
                                      signature='yyay')
            self.patterns.append(adv_pattern)


    def remove_monitor(self):
        self.remove_from_connection()


    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        print('{}: {} GetAll'.format(self.path, interface))
        if interface != ADV_MONITOR_IFACE:
            print('{}: GetAll: Invalid arg {}'.format(self.path, interface))
            return {}

        return self.get_properties()[ADV_MONITOR_IFACE]


    @dbus.service.method(ADV_MONITOR_IFACE,
                         in_signature='',
                         out_signature='')
    def Activate(self):
        print('{}: Monitor Activated'.format(self.path))


    @dbus.service.method(ADV_MONITOR_IFACE,
                         in_signature='',
                         out_signature='')
    def Release(self):
        print('{}: Monitor Released'.format(self.path))


    @dbus.service.method(ADV_MONITOR_IFACE,
                         in_signature='o',
                         out_signature='')
    def DeviceFound(self, device):
        print('{}: {} Device Found'.format(self.path, device))


    @dbus.service.method(ADV_MONITOR_IFACE,
                         in_signature='o',
                         out_signature='')
    def DeviceLost(self, device):
        print('{}: {} Device Lost'.format(self.path, device))


class AdvMonitorApp(dbus.service.Object):

    def __init__(self, bus, advmon_manager, app_id):
        self.bus = bus
        self.advmon_mgr = advmon_manager
        self.app_path = ADV_MONITOR_APP_BASE_PATH + str(app_id)

        self.monitors = dict()

        super(AdvMonitorApp, self).__init__(self.bus, self.app_path)


    def get_app_path(self):
        return dbus.ObjectPath(self.app_path)


    def add_monitor(self, monitor_data):
        monitor_id = 0
        while monitor_id in self.monitors:
            monitor_id += 1

        monitor = AdvMonitor(self.bus, self.app_path, monitor_id, monitor_data)

        # Emit the InterfacesAdded signal once the Monitor object is created.
        self.InterfacesAdded(monitor.get_path(), monitor.get_properties())

        self.monitors[monitor_id] = monitor

        return monitor_id


    def remove_monitor(self, monitor_id):
        monitor = self.monitors.pop(monitor_id, None)
        if not monitor:
            return False

        # Emit the InterfacesRemoved signal before removing the Monitor object.
        self.InterfacesRemoved(monitor.get_path(),
                               monitor.get_properties().keys())

        monitor.remove_monitor()

        return True


    def register_app(self):
        self.register_successful = None

        def register_cb():
            print('{}: RegisterMonitor successful'.format(self.app_path))
            self.register_successful = True

        def register_error_cb(error):
            print('{}: RegisterMonitor failed: {}'.format(self.app_path,
                                                          str(error)))
            self.register_successful = False

        self.advmon_mgr.RegisterMonitor(self.get_app_path(),
                                        reply_handler=register_cb,
                                        error_handler=register_error_cb)

        # Wait for the reply.
        while self.register_successful is None:
            pass

        return self.register_successful


    def unregister_app(self):
        self.unregister_successful = None

        def unregister_cb():
            print('{}: UnregisterMonitor successful'.format(self.app_path))
            self.unregister_successful = True

        def unregister_error_cb(error):
            print('{}: UnregisterMonitor failed: {}'.format(self.app_path,
                                                            str(error)))
            self.unregister_successful = False

        self.advmon_mgr.UnregisterMonitor(self.get_app_path(),
                                          reply_handler=unregister_cb,
                                          error_handler=unregister_error_cb)

        # Wait for the reply.
        while self.unregister_successful is None:
            pass

        return self.unregister_successful


    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        print('{}: GetManagedObjects'.format(self.app_path))
        objects = dict()
        for monitor_id in self.monitors:
            monitor = self.monitors[monitor_id]
            objects[monitor.get_path()] = monitor.get_properties()

        return objects


    @dbus.service.signal(DBUS_OM_IFACE, signature='oa{sa{sv}}')
    def InterfacesAdded(self, object_path, interfaces_and_properties):
        # Invoking this method emits the InterfacesAdded signal,
        # nothing needs to be done here.
        return


    @dbus.service.signal(DBUS_OM_IFACE, signature='oas')
    def InterfacesRemoved(self, object_path, interfaces):
        # Invoking this method emits the InterfacesRemoved signal,
        # nothing needs to be done here.
        return


def read_adapter_supported_monitor_types(adapter_props):
    types = json.dumps(adapter_props.Get(ADV_MONITOR_MANAGER_IFACE,
                       'SupportedMonitorTypes',
                       dbus_interface=DBUS_PROP_IFACE))
    return json.loads(types)


def read_adapter_supported_monitor_features(adapter_props):
    features = json.dumps(adapter_props.Get(ADV_MONITOR_MANAGER_IFACE,
                          'SupportedFeatures',
                          dbus_interface=DBUS_PROP_IFACE))
    return json.loads(features)


def print_supported_types_and_features(adapter_props):
    supported_types = read_adapter_supported_monitor_types(adapter_props)
    for supported_type in supported_types:
        print(supported_type)

    supported_features = read_adapter_supported_monitor_features(adapter_props)
    for supported_feature in supported_features:
        print(supported_feature)


def find_advmon_mgr(bus, adapter):
    return dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                          ADV_MONITOR_MANAGER_IFACE)


def find_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                                DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    adapter = None
    adapter_props = None

    for o, props in objects.items():
        if ADV_MONITOR_MANAGER_IFACE in props:
            adapter = o
            break

    if adapter:
        # Turn on the bluetooth adapter.
        adapter_props = dbus.Interface(
                                bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                DBUS_PROP_IFACE)
        adapter_props.Set('org.bluez.Adapter1', 'Powered', dbus.Boolean(1))

    return adapter, adapter_props


def test(bus, mainloop, advmon_mgr, app_id):
    # Create an App instance.
    app = AdvMonitorApp(bus, advmon_mgr, app_id)

    # Create two monitor objects before registering the app. No Activate() or
    # Release() should get called yet as the app is not registered.
    data0 = [
        'invalid_patterns',
        [-50, 1, -70, 1],
        [[0, 0x03, [0x12, 0x18]]] # Service Class UUID is 0x1812 (HOG)
    ]
    data1 = [
        'or_patterns',
        [127, 0, 127, 0],
        [[5, 0x09, [ord('_')]]] # 5th character of the Local Name is '_'
    ]
    monitor0 = app.add_monitor(data0)
    monitor1 = app.add_monitor(data1)

    # Register the app root path to expose advertisement monitors.
    # Release() should get called on monitor0 - incorrect monitor type.
    # Activate() should get called on monitor1.
    ret = app.register_app()
    if not ret:
        print('RegisterMonitor failed.')
        mainloop.quit()
        exit(-1)

    # Create two more monitor objects.
    # Release() should get called on monitor2 - incorrect RSSI Filter values.
    # Activate() should get called on monitor3.
    data2 = [
        'or_patterns',
        [-50, 1, -30, 1],
        [[0, 0x19, [0xC2, 0x03]]] # Appearance is 0xC203 (Mouse)
    ]
    data3 = [
        'or_patterns',
        [-50, 1, -70, 1],
        [[0, 0x03, [0x12, 0x18]], [0, 0x19, [0xC2, 0x03]]]
    ]
    monitor2 = app.add_monitor(data2)
    monitor3 = app.add_monitor(data3)

    # Run until user hits the 'Enter' key. If any peer device is advertising
    # during this time, DeviceFound() should get triggered for monitors
    # matching the advertisements.
    raw_input('Press "Enter" key to quit...\n')

    # Remove a monitor. DeviceFound() for this monitor should not get
    # triggered any more.
    app.remove_monitor(monitor1)

    # Unregister the app. Release() should get invoked on active monitors,
    # monitor3 in this case.
    app.unregister_app()

    mainloop.quit()


def main(app_id):
    # Initialize threads in gobject/dbus-glib before creating local threads.
    GObject.threads_init()
    dbus.mainloop.glib.threads_init()

    # Arrange for the GLib main loop to be the default.
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    mainloop = GObject.MainLoop()

    # Find bluetooth adapter and power it on.
    adapter, adapter_props = find_adapter(bus)
    if not adapter or not adapter_props:
        print('Bluetooth adapter not found.')
        exit(-1)

    # Read supported types and find AdvertisementMonitorManager1 interface.
    print_supported_types_and_features(adapter_props)
    advmon_mgr = find_advmon_mgr(bus, adapter)
    if not advmon_mgr :
        print('AdvertisementMonitorManager1 interface not found.')
        exit(-1)

    Thread(target=test, args=(bus, mainloop, advmon_mgr, app_id)).start()

    mainloop.run() # blocks until mainloop.quit() is called


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--app_id', default=0, type=int, help='use this App-ID '
                        'for creating dbus objects (default: 0)')
    args = parser.parse_args()

    main(args.app_id)
