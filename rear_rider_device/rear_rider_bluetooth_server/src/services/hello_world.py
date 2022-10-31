from bluez.example_gatt_server import GATT_CHRC_IFACE, Characteristic, Service, GObject, dbus
import subprocess

WLAN_INTERFACE = 'wlan'

class WifiAccessPoint():
    def __init__(self):
        pass
    
    def turn_off(self):
        ret = subprocess.call(['sudo', 'rfkill', 'block', WLAN_INTERFACE])
        return ret == 0
    
    def turn_on(self):
        ret = subprocess.call(['sudo', 'rfkill', 'unblock', WLAN_INTERFACE])
        return ret == 0
    
    def is_on(self):
        ret = subprocess.run(['sudo', 'rfkill'], stdout=subprocess.PIPE).stdout.decode('utf-8').split()
        return ret[8] == 'unblocked'

class HelloWorldService(Service):
    """
    A "hello world" service.
    """
    SENSORS_SVC_UUID = 'b4b1a70c-ba22-4e02-aba1-85d7e3171209'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.SENSORS_SVC_UUID, True)
        reverse_text_chr = ReverseTextCharacteristic(bus, 0, self)
        append_counter_chr = AppendCounterWithNotificationCharacteristic(bus, 1, self)
        config_chr = ConfigCharacteristic(bus, 2, self)
        wifi_chr = WifiCharacteristic(bus, 3, self)
        
        self.add_characteristic(reverse_text_chr)
        self.add_characteristic(append_counter_chr)
        self.add_characteristic(config_chr)
        self.add_characteristic(wifi_chr)
        
        self.reverse_text_chr = reverse_text_chr

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

class ConfigCharacteristic(Characteristic):
    """
    Configure the LED lights.
    """
    TEST_CHRC_UUID = '501beabd-3f66-4cca-ba7a-0fbf4f81870c'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.TEST_CHRC_UUID,
                ['write'],
                service)
        self.value = []

    def WriteValue(self, value, options):
        print('ConfigCharacteristic Write: ' + repr(value))
        self.value = value

class WifiCharacteristic(Characteristic):
    """
    Control Wi-Fi on Pi.
    """
    TEST_CHRC_UUID = 'cd41b278-6254-4c89-9cd1-fd2578ab8fcc'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.TEST_CHRC_UUID,
                ['read', 'write'],
                service)

    def ReadValue(self, options):
        wifi = WifiAccessPoint()
        if wifi.is_on():
            return dbus.ByteArray('1'.encode('utf8'))
        else:
            return dbus.ByteArray('0'.encode('utf8'))
    
    def WriteValue(self, value, options):
        wifi = WifiAccessPoint()
        # This formats the first byte of the dbus value to an integer.
        state = int(f'{value[0]}')
        if state == 0:
            wifi.turn_off()
        elif state == 1:
            wifi.turn_on()
