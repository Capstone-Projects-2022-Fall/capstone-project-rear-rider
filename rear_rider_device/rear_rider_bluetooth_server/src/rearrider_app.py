from rear_rider_device.rear_rider_bluetooth_server.src.bluez.example_gatt_server import Service, dbus, DBUS_OM_IFACE
from rear_rider_device.rear_rider_bluetooth_server.src.services.sensors import SensorsService
from rear_rider_device.rear_rider_bluetooth_server.src.services.hello_world import HelloWorldService
from rear_rider_device.rear_rider_bluetooth_server.src.services.actuators import ActuatorsService
from rear_rider_device.rear_rider_bluetooth_server.src.services.characteristics.strobe_light import StrobeLight

class RearRiderApplication(dbus.service.Object):
    """
    org.bluez.GattApplication1 interface implementation
    """
    services: list[Service]
    def __init__(self, bus, read_data, strobe_light: StrobeLight):
        self.path = '/'
        self.services = []
        dbus.service.Object.__init__(self, bus, self.path)

        hello_world_service = HelloWorldService(bus, 0)
        sensors_service = SensorsService(bus, 1, read_data)
        actuators_service = ActuatorsService(bus, 2, strobe_light)

        self.add_service(hello_world_service)
        self.add_service(sensors_service)
        self.add_service(actuators_service)
        
        self.hello_world_service = hello_world_service
        self.sensors_service = sensors_service

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service: Service):
        self.services.append(service)

    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
        print('GetManagedObjects')

        for service in self.services:
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
                descs = chrc.get_descriptors()
                for desc in descs:
                    response[desc.get_path()] = desc.get_properties()

        return response
