from rear_rider_device.rear_rider_bluetooth_server.src.services.hello_world import ConfigCharacteristic, LedConfig
import dbus
import unittest

class StubbedConfigCharacteristic(ConfigCharacteristic):
    """
    ConfigCharacteristic is stubbed so that a dbus object is not created.
    """
    def __init__(self): #pylint: disable=super-init-not-called
        self._config_characteristic__init__()

class TestConfigCharacteristic(unittest.TestCase):
    def test_set_on_led_config(self):
        callback_called = False
        config_val = [0x01, 0x01, 0xFF, 0xFF, 0xFF]
        def callback(new_led_config: LedConfig):
            nonlocal callback_called
            callback_called = True
            self.assertEqual(new_led_config.to_bytes(), config_val)
        test_cfg_chara = StubbedConfigCharacteristic()
        test_cfg_chara.set_on_led_config(callback=callback)
        test_cfg_chara.WriteValue(dbus.ByteArray(config_val), None)
        self.assertTrue(callback_called, 'The on_led_config callback was not called.')

def test_cases():
    return [
        TestConfigCharacteristic('test_set_on_led_config')
    ]