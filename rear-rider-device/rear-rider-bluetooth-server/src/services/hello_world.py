from bluez.example_gatt_server import GATT_CHRC_IFACE, Characteristic, Service, GObject, dbus

class HelloWorldService(Service):
    """
    A "hello world" service.
    """
    SENSORS_SVC_UUID = 'b4b1a70c-ba22-4e02-aba1-85d7e3171209'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.SENSORS_SVC_UUID, True)
        self.add_characteristic(ReverseTextCharacteristic(bus, 0, self))
        self.add_characteristic(AppendCounterWithNotificationCharacteristic(bus, 1, self))

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

class AppendCounterWithNotificationCharacteristic(Characteristic):
    """
    Appends a counter to a given text. Increments the counter everytime the paired device is notified.
    """
    UUID = '9f7bb8c9-4b29-4118-98ac-292557551cdf'
    value: dbus.ByteArray
    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.UUID,
            ['write', 'notify'],
            service)
        self.notifying = False
        self.value = dbus.ByteArray('default'.encode('utf8'))
        self.counter = 0

    def StartNotify(self):
        if self.notifying:
            print('Already in a notifying state.')
            return
        self.notifying = True
        self._start_appending_counter()

    def StopNotify(self):
        if not self.notifying:
            print('Not in a notifying state.')
            return
        self.notifying = False

    def WriteValue(self, value, options):
        self.value = value

    def _start_appending_counter(self):
        self.counter = 0
        GObject.timeout_add(1000, self._increment_counter)
    
    def _increment_counter(self):
        value = dbus.ByteArray('{}{}'
            .format(bytes(self.value).decode(), self.counter).encode('utf8'))
        self.PropertiesChanged(GATT_CHRC_IFACE, { 'Value': value }, [])
        self.counter += 1
        return self.notifying
