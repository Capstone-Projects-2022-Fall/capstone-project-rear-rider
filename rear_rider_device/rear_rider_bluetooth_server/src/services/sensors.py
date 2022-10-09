from bluez.example_gatt_server import Service

class SensorsService(Service):
    """
    TODO: Write documentation...
    """
    SENSORS_SVC_UUID = 'f0135e21-ad28-46e3-af7a-6e0829ab4c4a'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.SENSORS_SVC_UUID, True)
        # self.add_characteristic(CameraFeedCharacteristic(bus, 0, self))
        # self.add_characteristic(AccelerometerCharacteristic(bus, 1, self))
        # self.add_characteristic(RadarCharacteristic(bus, 2, self))

# class 