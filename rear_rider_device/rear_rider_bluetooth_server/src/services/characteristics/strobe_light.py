from dataclasses import dataclass
from typing import Callable
from bluez.example_gatt_server import Characteristic, Descriptor, dbus

@dataclass
class StrobeLight:
    """Represents the StrobeLight at any given time."""
    turn_on: Callable[[],None]
    turn_off: Callable[[],None]
    is_on: Callable[[],bool]
    frequency: int = 5

class StrobeLightCharacteristic(Characteristic):

    UUID = 'b5c29904-f59c-46b8-a045-a5a728bcceab'
    TURN_ON_UUID = '037f2be0-09eb-45da-9feb-750e1b1a1de8'
    TURN_OFF_UUID = 'c343530f-a972-43c4-beae-fc01afef5b28'

    def __init__(self, bus, index, service, config: StrobeLight):
        super().__init__(bus, index, self.UUID,
            ['read', 'writable-auxiliaries'], service)
        self._config = config
        # Add the descriptor that has a read trigger for turning on the strobe light.
        self.add_descriptor(ReadTriggerDescriptor(
            bus, 0, self,
            uuid=self.TURN_ON_UUID,
            on_trigger=self._turn_on
        ))
        # Add the descriptor that has a read trigger for turning off the strobe light.
        self.add_descriptor(ReadTriggerDescriptor(
            bus, 1, self,
            uuid=self.TURN_OFF_UUID,
            on_trigger=self._turn_off
        ))

        def frequency_setter(f: int):
            self._config.frequency = f
        def frequency_getter():
            return self._config.frequency
        self.add_descriptor(StrobeLightFrequencyDescriptor(
            bus, 2, self,
            frequency_getter=frequency_getter,
            frequency_setter=frequency_setter
        ))

    def ReadValue(self, options):
        """
        """
        return dbus.ByteArray(
            '{} {}'.format(
                self._config.frequency, self._config.is_on()
            ).encode('utf8'))
    
    def _turn_on(self) -> dbus.ByteArray:
        """
        Turn on the strobe light effect.
        0 for no errors, greater than 0 otherwise.
        """
        try:
            self._config.turn_on()
            return dbus.ByteArray([dbus.Boolean(0)])
        except:
            return dbus.ByteArray([dbus.Boolean(1)])
    
    def _turn_off(self) -> dbus.ByteArray:
        """
        Turn off the strobe light effect.
        0 for no errors, greater than 0 otherwise.
        """
        try:
            self._config.turn_off()
            return dbus.ByteArray([dbus.Boolean(0)])
        except:
            return dbus.ByteArray([dbus.Boolean(1)])


class StrobeLightFrequencyDescriptor(Descriptor):
    UUID = 'dd105fa6-3106-4e22-96a0-eae19e607454'

    def __init__(self, bus, index, characteristic,
            frequency_getter: Callable[[],int],
            frequency_setter: Callable[[int],None]):
        super().__init__(bus, index, self.UUID,
            ['read', 'write'],
            characteristic)
        self._get_frequency = frequency_getter
        self._set_frequency = frequency_setter
    
    def ReadValue(self, options):
        return dbus.ByteArray([dbus.UInt16(self._frequency)])
    
    def WriteValue(self, value, options):
        """
        Expects a dbus.String type
        """
        frequency = int(''.join(map(chr,value)))
        self._frequency = frequency
    
    @property
    def _frequency(self) -> int:
        return self._get_frequency()
    
    @_frequency.setter
    def _frequency(self, value: int):
        self._set_frequency(value)

class ReadTriggerDescriptor(Descriptor):
    """
    A descriptor that triggers an action when it is read from.
    """
    def __init__(self, bus, index, characteristic, uuid: str, on_trigger: Callable[[], dbus.ByteArray]):
        """
        on_trigger:
            A callback that is triggered when the descriptor is read.
        """
        super().__init__(bus, index, uuid,
                ['read'],
                characteristic)
        self._on_trigger = on_trigger
    
    def ReadValue(self, options):
        """
        """
        return self._on_trigger()

# class LEDBrightnessDescriptor(Descriptor):
#     def __init__(self, bus, index, characteristic):
#         super().__init__(bus, index, self.,
#                 ['read', 'write'], characteristic)
