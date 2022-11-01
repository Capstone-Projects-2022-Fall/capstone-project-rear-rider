from bluez.example_gatt_server import Service
from services.characteristics.strobe_light import StrobeLightCharacteristic, StrobeLight


class ActuatorsService(Service):

    ACTUATORS_SVC_UUID = '75d57431-560d-4449-93fd-ba5f9fe663d9'
    def __init__(self, bus, index, strobe_light: StrobeLight):
        super().__init__(bus, index, self.ACTUATORS_SVC_UUID, True)
        self._strobe_light = StrobeLightCharacteristic(
            bus, 0, self, strobe_light)
        self.add_characteristic(self._strobe_light)
