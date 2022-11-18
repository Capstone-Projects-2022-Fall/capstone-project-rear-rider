from typing import Callable
from rear_rider_device.rear_rider_bluetooth_server.src.bluez.example_gatt_server import GATT_CHRC_IFACE, Characteristic, Service, GObject
import dbus

class LidarCharacteristic(Characteristic):
    UUID = '92cb916f-d996-4f30-8cba-cf3ab8aede56'
    def __init__(self, bus, index, service, read_data: Callable[[], str]):
        super().__init__(bus, index, self.UUID,
            ['notify'], service)
        self.notifying = False
        self.read_data = read_data
        self.value = []
    
    def StartNotify(self):
        if self.notifying:
            return
        self.notifying = True
    
    def StopNotify(self):
        if not self.notifying:
            return
        self.notifying = False
    
    def object_notify(self, distance):
        self.PropertiesChanged(GATT_CHRC_IFACE, { 'Value': dbus.UInt16(distance)}, [])
