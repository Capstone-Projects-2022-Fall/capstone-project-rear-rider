from rear_rider_device.rear_rider_bluetooth_server.src.bluez.example_advertisement import Advertisement

class RearRiderAdvertisement(Advertisement):
    
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        self.add_manufacturer_data(0xfff0, [0x03, 0x02, 0x01, 0x00])
        print(self.manufacturer_data)
        self.add_local_name('RearRiderPi4')
        # self.include_tx_power = True
        # self.add_data(0x26, [0x01, 0x01, 0x00])
