from sys import stdout
import dbus
from typing import Callable
from rear_rider_device.rear_rider_bluetooth_server.src.bluez.example_gatt_server import GATT_CHRC_IFACE, Characteristic, Service, GObject

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
            # print('DATA: {}'.format(value))
            return self.notifying
            
        GObject.timeout_add(1000, notify)
    
    def StopNotify(self):
        if not self.notifying:
            return
        self.notifying = False

    def ReadValue(self, options):
        # TODO: Move this into a callback function.
        line = 'accelerometer'
        if line != 'accelerometer':
            return
        stdout.write('read_accelerometer\n')
        stdout.flush()
        nums = self.vector
        
        data = self._get_vector_data()
        # print(data)
        return data
    
    def _get_vector_data(self):
        """
        As a byte string in ut8.
        """
        nums = self.vector
        return dbus.ByteArray('{},{},{}'.format(
            nums[0], nums[1], nums[2]
        ).encode('utf8'))