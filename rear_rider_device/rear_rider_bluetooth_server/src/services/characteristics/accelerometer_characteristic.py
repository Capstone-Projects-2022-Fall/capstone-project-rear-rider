from typing import Callable, Union
import dbus
from rear_rider_device.rear_rider_bluetooth_server.src.bluez.example_gatt_server import \
    GATT_CHRC_IFACE, Characteristic, Descriptor, FailedException
from rear_rider_device.utils.threaded_repeat import ThreadedRepeat


class AccelerometerCharacteristic(Characteristic):
    UUID = '6df2bcb1-a775-42ea-91c2-14d22c1c8f48'
    def __init__(self, bus, index, service):
        super().__init__(bus, index, self.UUID,
            ['read', 'write', 'notify'], service)
        self._read_accelerometer_cb: Union[None, Callable[[], tuple[float, float, float]]] = None
        self._accel: tuple[float, float, float] = (0.0,0.0,0.0)
        self._notifier: Union[None, ThreadedRepeat] = None
        self._accelerometer_notify_interval = AccelerometerNotifyIntervalDescriptor(
            bus, 0, self
        )
        def on_accel_notify_interval_change(interval_ms: int):
            try:
                self._notifier.update_interval(interval_seconds=interval_ms/1000.0) # type: ignore
            except:
                # try block may throw if _notifier is None. Since it may be set to None by another
                # thread let's avoid using a mutex lock by just catching and passing the exception.
                pass
        self._accelerometer_notify_interval.set_on_change_cb(on_accel_notify_interval_change)
        self.descriptors.append(self._accelerometer_notify_interval)


    def StartNotify(self):
        if self._notifier is not None:
            return
        def notify():
            self.PropertiesChanged(GATT_CHRC_IFACE, {
                'Value': self._read_accelerometer()
            }, [])
        self._notifier = ThreadedRepeat(self._accelerometer_notify_interval.get_interval()/1000,
                notify)
        self._notifier.start()

    def StopNotify(self):
        if self._notifier is None:
            return
        self._notifier.cancel()
        self._notifier = None

    def ReadValue(self, options):
        return self._read_accelerometer()

    def _read_accelerometer(self):
        '''
        Raises an 'org.bluez.Error.Failed' error if there was no callback assigned via
        `self.set_read_accelerometer_cb(...)`.

        The value is read, `self.vector` is set to that value, then it is formatted as a dbus byte
        array type (which is encoded as a utf8 string) and returned.
        '''
        if self._read_accelerometer_cb is None:
            raise FailedException('The callback to read the accelerometer data is None.')
        self._accel = self._read_accelerometer_cb()
        return _dbus_format_accel_vector(self._accel)

    def set_read_accelerometer_cb(self, callback: Callable[[],tuple[float, float, float]]):
        '''
        Sets the callback function for when the bluetooth characteristic is being accessed for 
        reads or for acquire-notifications.
        '''
        self._read_accelerometer_cb = callback

def _dbus_format_accel_vector(vector: tuple[float, float, float]):
    '''
    Format a 3 vector tuple as a dbus ByteArray type (a utf 8 string).
    '''
    return dbus.ByteArray(f'{vector[0]},{vector[1]},{vector[2]}'.encode('utf8'))

class AccelerometerNotifyIntervalDescriptor(Descriptor):
    UUID = 'e01f9dab-64c6-429f-8e89-3f185392c327'

    def __init__(self, bus, index, characteristic, interval_ms=1000):
        super().__init__(bus, index, self.UUID,
            ['read', 'write'],
            characteristic)
        self._interval_ms = interval_ms
        '''
        In milliseconds.
        '''
        self._on_change_cb: Union[None, Callable[[int], None]] = None
    
    def ReadValue(self, options):
        try:
            return dbus.ByteArray(dbus.UInt16(self._interval_ms).to_bytes(2, 'big'))
        except Exception as e:
            print(e)
    
    def WriteValue(self, value, options):
        """
        Expects bytes representing a uint16 in big-endian ordering.
        """
        interval = int.from_bytes(value, 'big')
        self._interval_ms = interval
        if self._on_change_cb is not None:
            self._on_change_cb(interval)
    
    def set_on_change_cb(self, callback: Callable[[int], None]):
        self._on_change_cb = callback

    def get_interval(self):
        '''
        Get the interval in milliseconds.
        '''
        return self._interval_ms
