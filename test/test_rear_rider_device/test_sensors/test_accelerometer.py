from rear_rider_device.rear_rider_sensors.accelerometer import Accelerometer

def test_accelerometer():
    x = Accelerometer()
    print(x.get_acceleration())