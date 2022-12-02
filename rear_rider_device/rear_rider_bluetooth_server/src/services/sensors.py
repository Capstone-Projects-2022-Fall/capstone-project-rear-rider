from typing import Callable
from rear_rider_device.rear_rider_bluetooth_server.src.bluez.example_gatt_server import Service
from rear_rider_device.rear_rider_bluetooth_server.src.services.characteristics.\
    accelerometer_characteristic import AccelerometerCharacteristic

class SensorsService(Service):
    """
    TODO: Write documentation...
    """
    SENSORS_SVC_UUID = 'f0135e21-ad28-46e3-af7a-6e0829ab4c4a'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.SENSORS_SVC_UUID, True)
        accelerometer_characteristic = AccelerometerCharacteristic(
            bus, 0, self)

        # self.add_characteristic(CameraFeedCharacteristic(bus, 0, self))
        self.add_characteristic(accelerometer_characteristic)
        # self.add_characteristic(RadarCharacteristic(bus, 2, self))

        self.accelerometer_characteristic = accelerometer_characteristic
