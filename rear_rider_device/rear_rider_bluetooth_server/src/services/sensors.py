from sys import stdin, stdout
from typing import Callable
from bluez.example_gatt_server import dbus, GATT_CHRC_IFACE, Characteristic, Service, GObject

class SensorsService(Service):
    """
    TODO: Write documentation...
    """
    SENSORS_SVC_UUID = 'f0135e21-ad28-46e3-af7a-6e0829ab4c4a'

    def __init__(self, bus, index, read_data: Callable[[], str]):
        Service.__init__(self, bus, index, self.SENSORS_SVC_UUID, True)
        accelerometer_characteristic = AccelerometerCharacteristic(
            bus, 0, self, read_data=read_data)

        # self.add_characteristic(CameraFeedCharacteristic(bus, 0, self))
        self.add_characteristic(accelerometer_characteristic)
        # self.add_characteristic(RadarCharacteristic(bus, 2, self))

        self.accelerometer_characteristic = accelerometer_characteristic

class AccelerometerCharacteristic(Characteristic):
    UUID = '6df2bcb1-a775-42ea-91c2-14d22c1c8f48'
    def __init__(self, bus, index, service, read_data: Callable[[], str]):
        super().__init__(bus, index, self.UUID,
            ['read', 'write', 'notify'], service)
        self.notifying = False
        self.read_data = read_data
        self.value = []
        self.vector: tuple[float, float, float] = (0.0,0.0,0.0)
    
    def StartNotify(self):
        if self.notifying:
            return
        self.notifying = True
        def notify():
            value = self._get_vector_data()
            self.PropertiesChanged(GATT_CHRC_IFACE, { 'Value': value }, [])
            print('DATA: {}'.format(value))
            return self.notifying
            
        GObject.timeout_add(1000, notify)
    
    def StopNotify(self):
        if not self.notifying:
            return
        self.notifying = False

    def ReadValue(self, options):
        line = 'accelerometer'
        if line != 'accelerometer':
            return
        stdout.write('read_accelerometer\n')
        stdout.flush()
        nums = self.vector
        
        data = self._get_vector_data()
        print(data)
        return data
    
    def _get_vector_data(self):
        """
        As a byte string in ut8.
        """
        nums = self.vector
        return dbus.ByteArray('{},{},{}'.format(
            nums[0], nums[1], nums[2]
        ).encode('utf8'))
    

