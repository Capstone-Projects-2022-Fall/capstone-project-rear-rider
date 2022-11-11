// RearRider
//
// Calin Pescaru
//
// October 2022
//
// Bluetooth Manager
//
// Manages a Bluetooth connection to RaspberryPi.

import Foundation
import CoreBluetooth
import UIKit
import SwiftUI


let piName = "RearRiderPi4"

/// Structure holding the UUIDs required for connecting to the peripheral (RaspberryPi)
struct CBUUIDs {
    static let BLEServiceUUID = CBUUID(string: "b4b1a70c-ba22-4e02-aba1-85d7e3171209")
    static let BLECharacteristicUUID = CBUUID(string: "3bd0b2f7-72f8-4497-bbe5-6bc3db448b95")
    static let BLENotifyCharacteristicUUID = CBUUID(string: "9f7bb8c9-4b29-4118-98ac-292557551cdf")
    static let BLEConfigCharacteristicUUID = CBUUID(string: "501beabd-3f66-4cca-ba7a-0fbf4f81870c")
    static let BLEWifiCharacteristicUUID = CBUUID(string: "cd41b278-6254-4c89-9cd1-fd2578ab8fcc")
    static let BLEPictureCharacteristicUUID = CBUUID(string: "cd41b278-6254-4c89-9cd1-fd2578ab8abb")
}

/// The purpose of this class is to set the iPhone as a central manager and connect to the RaspberryPi as a peripheral
/// When a connection is successful, a String message can be passed between the endpoints
class BLEManager: NSObject, ObservableObject, CBCentralManagerDelegate, CBPeripheralDelegate, CBPeripheralManagerDelegate {
    private var myCentral: CBCentralManager!
    private var myPeripheral: CBPeripheral!
    private var reverseCharacteristic: CBCharacteristic!
    private var notifyCharacteristic: CBCharacteristic!
    private var configCharacteristic: CBCharacteristic!
    private var wifiCharacteristic: CBCharacteristic!
    private var picCharacteristic: CBCharacteristic!
    
    //mostly for testing purposes
    var ConfigCharacteristic: CBCharacteristic {
        get {
            return configCharacteristic
        }
    }
    
    var WiFiCharacteristic: CBCharacteristic {
        get {
            return wifiCharacteristic
        }
    }
    
    static var shared = BLEManager()
    private let log = RearRiderLog.shared
    private var pic_index: UInt8 = 0; // current index of the picture packet transfer
    
    @Published var isSwitchedOn = false
    @Published var connected = false
    
    /// Initialize the base class (NSObject) and CBCentralManager
    override init() {
        super.init()
        myCentral = CBCentralManager(delegate: self, queue: nil)
        myCentral.delegate = self
    }
    
    /// Called when the state of the central manager is changed
    /// - Parameter central: a CBCentralManager (the client in a Bluetooth architecture)
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        if central.state == .poweredOn {
            isSwitchedOn = true
            self.startScanning()
        }
        else {
            isSwitchedOn = false
        }
    }
    
    /// Called when the state of the peripheral is changed
    /// - Parameter peripheral: a CBPeripheralManager (the server)
    func peripheralManagerDidUpdateState(_ peripheral: CBPeripheralManager) {
        if peripheral.state == .poweredOn {
            print("Peripheral is powered on")
        }
    }
    
    /// Called when a peripheral is discovered; when the RaspberryPi is discovered it will attempt to connect to it
    /// - Parameters:
    ///   - central: a CBCentralManager (iPhone)
    ///   - peripheral: a CBPeripheral (RaspberryPi)
    ///   - advertisementData: an array of Strings that describe the advertisement data
    ///   - RSSI: a NSNumber describing the signal strength
    func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral,
                        advertisementData: [String: Any], rssi RSSI: NSNumber) {
        if peripheral.name != nil && peripheral.name == piName {
            log.addLog(from: "BT", message: "Found \(peripheral.name!)")
            myPeripheral = peripheral
            myPeripheral.delegate = self

            myCentral?.stopScan()
            log.addLog(from: "BT", message: "Scanning stopped")

            myCentral?.connect(myPeripheral!, options: nil)
            log.addLog(from: "BT", message: "Connecting to RaspberryPi")
        }
    }
    
    /// Scans for peripherals
    func startScanning() {
        print("startScanning")
        log.addLog(from: "BT", message: "Scanning started")
        log.addLog(from: "BT", message: "Looking for RaspberryPi")
        myCentral?.scanForPeripherals(withServices: nil, options: nil)
    }
    
    /// Stops scanning
    func stopScanning() {
        print("stopScanning")
        log.addLog(from: "BT", message: "Scanning stopped")
        myCentral?.stopScan()
    }
    
    /// Sends a message to the connected peripheral by writing to the characteristic
    /// - Parameter msg: a String containing the message to be sent
    func sendMsg(message msg: String) {
        if myPeripheral != nil  && !msg.isEmpty {
            log.addLog(from: "BT", message: "Sent: " + msg)
        
            let valueString = (msg as NSString).data(using: String.Encoding.utf8.rawValue)
            myPeripheral.writeValue(valueString!, for: reverseCharacteristic, type: CBCharacteristicWriteType.withResponse)
            myPeripheral.readValue(for: reverseCharacteristic)
        }
    }
    
    /// Disconnect from the peripheral
    func disconnectBLE() {
        if myPeripheral != nil {
            print("Disconnecting...")
            myCentral?.cancelPeripheralConnection(myPeripheral!)
            log.addLog(from: "BT", message: "Disconnected")
            connected = false
        }
    }
    
    /// Called when a connection is successful; then it begins discovering services
    /// - Parameters:
    ///   - central: a CBCentralManager (iPhone)
    ///   - peripheral: a CBPeripheral (RaspberryPi)
    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        myPeripheral.discoverServices([CBUUIDs.BLEServiceUUID])
        log.addLog(from: "BT", message: "Connection successful")
        log.addLog(from: "BT", message: "Discovering services")
    }
    
    /// Called when services are discovered; then it begins discovering characteristics
    /// - Parameters:
    ///   - peripheral: a CBPeripheral (RaspberryPi)
    ///   - error: an Error type; holds information about the error, if any
    func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
        if error != nil {
            print("Error discovering services: \(error!.localizedDescription)")
            log.addLog(from: "BT", message: "Error discovering services!")
            return
        }
        
        guard let services = peripheral.services else {
            return
        }
        
        for service in services {
            peripheral.discoverCharacteristics(nil, for: service)
        }
        print("Discovered Services: \(services)")
        log.addLog(from: "BT", message: "Services discovered")
    }
    
    /// Called when characteristics are discovered
    /// - Parameters:
    ///   - peripheral: a CBPeripheral (RaspberryPi)
    ///   - service: a CBService
    ///   - error: an Error type; holds information about the error, if any
    func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {
        guard let characteristics = service.characteristics else {
            return
        }
        
        print("Found \(characteristics.count) characteristics.")
        log.addLog(from: "BT", message: "Found \(characteristics.count) characteristics.")
        
        for characteristic in characteristics {
            print(characteristic.description)
            
            if characteristic.uuid.isEqual(CBUUIDs.BLECharacteristicUUID) {
                reverseCharacteristic = characteristic
                log.addLog(from: "BT", message: "Reverse Characteristic set")
                connected = true
            }
            else if characteristic.uuid.isEqual(CBUUIDs.BLENotifyCharacteristicUUID) {
                notifyCharacteristic = characteristic
                log.addLog(from: "BT", message: "Notify Characteristic set")
                connected = true
            }
            else if characteristic.uuid.isEqual(CBUUIDs.BLEConfigCharacteristicUUID) {
                configCharacteristic = characteristic
                log.addLog(from: "BT", message: "Config Characteristic set")
                connected = true
            }
            else if characteristic.uuid.isEqual(CBUUIDs.BLEWifiCharacteristicUUID) {
                wifiCharacteristic = characteristic
                log.addLog(from: "BT", message: "Wi-Fi Characteristic set")
                connected = true
                peripheral.setNotifyValue(true, for: wifiCharacteristic)
                isWifiOn()
            }
            else if characteristic.uuid.isEqual(CBUUIDs.BLEPictureCharacteristicUUID) {
                picCharacteristic = characteristic
                log.addLog(from: "BT", message: "Picture Characteristic set")
                connected = true
            }
        }
    }
    
    /// Called when the value of a characterisitc is updated and appends the value to the messages array
    /// - Parameters:
    ///   - peripheral: a CBPeripheral
    ///   - characteristic: a CBCharacteristic
    ///   - error: an Error type; holds information about the error, if any
    func peripheral(_ peripheral: CBPeripheral, didUpdateValueFor characteristic: CBCharacteristic, error: Error?) {
        if characteristic == reverseCharacteristic {
            let ASCIIString = NSString(data: characteristic.value ?? Data(), encoding: String.Encoding.utf8.rawValue)
            log.addLog(from: "BT", message: "Recv(reverse): \(ASCIIString! as String)")
            print("Value received \(ASCIIString! as String).")
        }
        else if characteristic == notifyCharacteristic {
            let ASCIIString = NSString(data: characteristic.value ?? Data(), encoding: String.Encoding.utf8.rawValue)
            log.addLog(from: "BT", message: "Recv(notify): \(ASCIIString! as String)")
            print("Value received \(ASCIIString! as String).")
        }
        else if characteristic == wifiCharacteristic {
            let ASCIIString = NSString(data: characteristic.value ?? Data(), encoding: String.Encoding.utf8.rawValue)
            print("Value received \(ASCIIString! as String).")
            log.addLog(from: "BT", message: "Recv(wifi): \(ASCIIString! as String).")
            if ASCIIString!.contains("1") {
                WifiManager.shared.setWifi(isOn: true)
            }
            else {
                WifiManager.shared.setWifi(isOn: false)
            }
        }
        else if characteristic == picCharacteristic {
            if RearRiderAlerts.shared.pic_first_time {
                pic_index = 0
                let d = String(data: characteristic.value ?? Data(), encoding: String.Encoding.utf8)
                if d!.count > 0 {
                    RearRiderAlerts.shared.pic_first_time = false
                    let components = d?.components(separatedBy: "-")
                    RearRiderAlerts.shared.pic_size = Int(components![0]) ?? 0
                    RearRiderAlerts.shared.pic_packets = Int(components![1]) ?? 0
                }
            }
            else {
                let d: Data = characteristic.value ?? Data()
                if d.count > 0 {
                    RearRiderAlerts.shared.picData.append(d)
                    RearRiderAlerts.shared.packet_recv = pic_index + 1
                    pic_index += 1
                }
            }
        }
    }
    
    /// Called when the state of the connection changes
    /// - Parameters:
    ///   - peripheral: a CBPeripheral
    ///   - invalidatedServices: an array of CBServices
    func peripheral(_ peripheral: CBPeripheral, didModifyServices invalidatedServices: [CBService]) {
        connected = false
        log.addLog(from: "BT", message: "RPi disconnected")
    }
    
    /// Called when the peripheral disconnects
    /// - Parameters:
    ///   - central: a CBCentralManager
    ///   - peripheral: a CBPeripheral
    ///   - error: an Error type; holds information about the error, if any
    func centralManager(_ central: CBCentralManager, didDisconnectPeripheral peripheral: CBPeripheral, error: Error?) {
        if peripheral == myPeripheral {
            guard peripheral.state == .disconnected else { return }
            print("RPi disconnected")
            log.addLog(from: "BT", message: "RPi disconnected")
            connected = false
        }
    }
    
    /// Toggle on/off the notify option for the notifyCharacteristic
    /// - Parameter e: a Bool type: true or false
    func toggleNotifyCharacteristic(enabled e: Bool) {
        myPeripheral.setNotifyValue(e, for: notifyCharacteristic)
    }
    
    /// This function sends the configuration from the settings over BT to the Pi
    /// - Parameter bytes: a Data type that is an array of bytes
    func sendConfigToPi(data bytes: Data) {
        if connected {
            myPeripheral.writeValue(bytes, for: configCharacteristic, type: CBCharacteristicWriteType.withResponse)
            log.addLog(from: "BT", message: "Configuration sent to Pi")
        }
        else {
            print("Cannot send config to Pi. Not connected!")
            log.addLog(from: "BT", message: "Cannot send config to Pi. Not connected!")
        }
    }
    
    /// Interrogates the Pi to find out if the Wi-Fi is on
    func isWifiOn() {
        if connected {
            myPeripheral.readValue(for: wifiCharacteristic)
        }
    }
    
    /// Sends a command over BT to tell the Pi to turn on its Wi-Fi
    func turnWifiOn() {
        if connected {
            var data = Data()
            var on: UInt8 = 1
            data.append(withUnsafeBytes(of: &on) { Data($0) })
            myPeripheral.writeValue(data, for: wifiCharacteristic, type: CBCharacteristicWriteType.withResponse)
            isWifiOn()
        }
    }
    
    /// Sends a command over BT to tell the Pi to turn off its Wi-Fi
    func turnWifiOff() {
        if connected {
            var data = Data()
            var off: UInt8 = 0
            data.append(withUnsafeBytes(of: &off) { Data($0) })
            myPeripheral.writeValue(data, for: wifiCharacteristic, type: CBCharacteristicWriteType.withResponse)
            isWifiOn()
        }
    }
    
    /// Initiates the picture transfer. First piece of data received will be the size and the number of packets
    func getPicInfo() {
        if connected {
            myPeripheral.readValue(for: picCharacteristic)
        }
    }
    
    /// Sends command over BT to ask for a packet to be transferred
    /// - Parameter i: a UInt8 describing the index of the packet to retrieve
    func getPicPacket(index i: UInt8) {
        if connected {
            var data = Data()
            var index: UInt8 = i // due to the function below does not accepting the constant i
            data.append(withUnsafeBytes(of: &index) { Data($0) })
            myPeripheral.writeValue(data, for: picCharacteristic, type: CBCharacteristicWriteType.withResponse)
            myPeripheral.readValue(for: picCharacteristic)
        }
    }
}
