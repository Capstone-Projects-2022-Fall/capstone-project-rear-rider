from bluez.example_gatt_server import Characteristic, Service

class HelloWorldService(Service):
    """
    A "hello world" service.
    """
    SENSORS_SVC_UUID = 'b4b1a70c-ba22-4e02-aba1-85d7e3171209'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.SENSORS_SVC_UUID, True)
        self.add_characteristic(ReverseTextCharacteristic(bus, 0, self))

class ReverseTextCharacteristic(Characteristic):
    """
    Reverses a given text.
    """
    TEST_CHRC_UUID = '3bd0b2f7-72f8-4497-bbe5-6bc3db448b95'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.TEST_CHRC_UUID,
                ['read', 'write', 'writable-auxiliaries'],
                service)
        self.value = []
        # self.add_descriptor(TestDescriptor(bus, 0, self))

    def ReadValue(self, options):
        print('TestCharacteristic Read: ' + repr(self.value))
        return self.value

    def WriteValue(self, value, options):
        print('TestCharacteristic Write: ' + repr(value))
        self.value = value[::-1]