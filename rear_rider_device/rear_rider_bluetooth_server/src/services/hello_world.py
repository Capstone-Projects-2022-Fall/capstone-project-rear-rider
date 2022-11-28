from dataclasses import dataclass
from typing import Callable, Union
from rear_rider_device.rear_rider_bluetooth_server.src.bluez.example_gatt_server import GATT_CHRC_IFACE, Characteristic, Service, GObject, dbus
import subprocess

from picamera2 import Picamera2
import io
import math
from PIL import Image

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
        pic_chr = PictureCharacteristic(bus, 4, self)
        lidar_chr = LiDARCharacteristic(bus, 5, self)

        self.add_characteristic(reverse_text_chr)
        self.add_characteristic(append_counter_chr)
        self.add_characteristic(config_chr)
        self.add_characteristic(wifi_chr)
        self.add_characteristic(pic_chr)
        self.add_characteristic(lidar_chr)
        
        self.reverse_text_chr = reverse_text_chr
        self.config_chr = config_chr
        self.lidar_chr = lidar_chr

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

@dataclass
class LedConfig:
    pattern: int = 0
    """
    0 - no pattern
    """
    brightness: int = 0
    """
    1 - low
    2 - medium
    3 - high
    """
    color: tuple[int,int,int] = (255, 255, 255)
    """
    (r, g, b)
    """

    def to_bytes(self):
        return [self.pattern, self.brightness, *self.color]

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
        self.value: LedConfig
        self._on_led_config: Union[None, Callable[[LedConfig], None]] = None
        self._config_characteristic__init__()
    
    def _config_characteristic__init__(self):
        self.value = LedConfig()

    def WriteValue(self, value, options):
        pattern = int(value[0])
        brightness = int(value[1])
        r = int(value[2])
        g = int(value[3])
        b = int(value[4])
        # print(f'ConfigCharacteristic Write: {pattern} {brightness} {r} {g} {b}')
        self.value = LedConfig(pattern, brightness, (r, g, b))
        if self._on_led_config is not None:
            self._on_led_config(self.value)
    
    def set_on_led_config(self, callback: Callable[[LedConfig], None]):
        self._on_led_config = callback


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
        state = int(value[0])
        if state == 0:
            # wifi.turn_off()
            pass
        elif state == 1:
            wifi.turn_on()

class PictureCharacteristic(Characteristic):
    """
    Send one frame from the camera.
    """
    TEST_CHRC_UUID = 'cd41b278-6254-4c89-9cd1-fd2578ab8abb'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.TEST_CHRC_UUID,
                ['read', 'write'],
                service)
        
        self.first_time = True # first time send the size of pic and the number of packets
        self.packets = 0
        self.packet_size = 512 # number of bytes in one packet
        self.buff_size = 0
        self.data = io.BytesIO()
        self.dataList = [] # convert data into a list of packets each of packet_size size
        self.value = 0 # the index in dataList
    
    """
    Write log for debugging
    """
    def write_log(self, s):
        self.f.write(s)
        self.f.write('\n')
        self.f.flush()

    def ReadValue(self, options):
        if self.packets == 0:
            # reset
            self.first_time = True
            self.dataList = []
            self.data = io.BytesIO()
            
            # take picture
            cam = Picamera2()
            config = cam.create_preview_configuration(main={"size": (320, 240)})
            cam.configure(config)
            cam.start()
            cam.capture_file(self.data, format='jpeg')
            cam.close()
            
            # compress image
            img = Image.open(self.data)
            self.data = io.BytesIO() # have to reset data; otherwise the next function doesn't replace the contents of data
            img.save(self.data, 'JPEG', quality=50)
            
            self.buff_size = len(self.data.getvalue())
            self.packets = math.floor(self.buff_size / self.packet_size)
            if self.packets % self.buff_size: # if the division has remainder add one more packet
                self.packets = self.packets + 1
            
            start = 0
            end = self.packet_size
            
            # split self.data into a list
            for i in range(0, self.packets):
                self.dataList.append(self.data.getvalue()[start:end])
                start = start + self.packet_size
                end = end + self.packet_size # if it doesn't work change the last packet to buff_size - start
        
        if self.first_time:
            self.first_time = False
            msg = str(self.buff_size) + '-' + str(self.packets)
            return dbus.Array(msg.encode('utf8'))
        else:
            self.packets = self.packets - 1
            return dbus.Array(self.dataList[self.value], signature='y')
    
    def WriteValue(self, value, options):
        self.value = int(value[0])

class LiDARCharacteristic(Characteristic):
    """
    Notifies the iOS app when an object is detected by the LiDAR sensor and sends
    the distance.
    """
    UUID = '92cb916f-d996-4f30-8cba-cf3ab8aede56'
    value: dbus.ByteArray
    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.UUID,
            ['notify'],
            service)
        self.notifying = False
        self.value = 0

    def StartNotify(self):
        if self.notifying:
            print('Already in a notifying state.')
            return
        self.notifying = True

    def StopNotify(self):
        if not self.notifying:
            print('Not in a notifying state.')
            return
        self.notifying = False
    
    def check_object_in_range(self):
        value = dbus.ByteArray(self.value.encode('utf8'))
        self.PropertiesChanged(GATT_CHRC_IFACE, { 'Value': value }, [])
        return self.notifying
