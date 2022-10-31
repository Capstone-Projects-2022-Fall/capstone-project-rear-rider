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


let piName = "RearRiderPi4"


/// Structure for status messages; conforms to the Identifiable protocol
struct StatusMsg: Identifiable {
    let id: Int
    let msg: String
}

/// Structure for communication messages; conforms to the Identifiable protocol
struct Message: Identifiable {
    let id: Int
    let msg: String
}

/// Structure holding the UUIDs required for connecting to the peripheral (RaspberryPi)
struct CBUUIDs {
    static let BLEServiceUUID = CBUUID(string: "b4b1a70c-ba22-4e02-aba1-85d7e3171209")
    static let BLECharacteristicUUID = CBUUID(string: "3bd0b2f7-72f8-4497-bbe5-6bc3db448b95")
    static let BLENotifyCharacteristicUUID = CBUUID(string: "9f7bb8c9-4b29-4118-98ac-292557551cdf")
}

/// The purpose of this class is to set the iPhone as a central manager and connect to the RaspberryPi as a peripheral
/// When a connection is successful, a String message can be passed between the endpoints
class BLEManager: NSObject, ObservableObject, CBCentralManagerDelegate, CBPeripheralDelegate, CBPeripheralManagerDelegate {
    private var myCentral: CBCentralManager!
    private var myPeripheral: CBPeripheral!
    private var reverseCharacteristic: CBCharacteristic!
    private var notifyCharacteristic: CBCharacteristic!
    
    @Published var isSwitchedOn = false
    @Published var connected = false
    @Published var messages = [Message]()
    @Published var statusMsgs = [StatusMsg]()
    
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
            addStatusMessage(message: "Found \(peripheral.name!)")
            myPeripheral = peripheral
            myPeripheral.delegate = self

            myCentral?.stopScan()
            addStatusMessage(message: "Scanning stopped")

            myCentral?.connect(myPeripheral!, options: nil)
            addStatusMessage(message: "Connecting to RaspberryPi")
        }
    }
    
    /// Scans for peripherals
    func startScanning() {
        print("startScanning")
        addStatusMessage(message: "Scanning started")
        addStatusMessage(message: "Looking for RaspberryPi")
        myCentral?.scanForPeripherals(withServices: nil, options: nil)
    }
    
    /// Stops scanning
    func stopScanning() {
        print("stopScanning")
        myCentral?.stopScan()
    }
    
    /// Sends a message to the connected peripheral by writing to the characteristic
    /// - Parameter msg: a String containing the message to be sent
    func sendMsg(message msg: String) {
        if myPeripheral != nil  && !msg.isEmpty {
            let newMessage = Message(id: messages.count, msg: "P: " + msg)
            messages.append(newMessage)
        
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
            addStatusMessage(message: "Disconnected")
        }
    }
    
    /// Called when a connection is successful; then it begins discovering services
    /// - Parameters:
    ///   - central: a CBCentralManager (iPhone)
    ///   - peripheral: a CBPeripheral (RaspberryPi)
    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        myPeripheral.discoverServices([CBUUIDs.BLEServiceUUID])
        addStatusMessage(message: "Connection successful")
        addStatusMessage(message: "Discovering services")
    }
    
    /// Called when services are discovered; then it begins discovering characteristics
    /// - Parameters:
    ///   - peripheral: a CBPeripheral (RaspberryPi)
    ///   - error: an Error type; holds information about the error, if any
    func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
        if error != nil {
            print("Error discovering services: \(error!.localizedDescription)")
            addStatusMessage(message: "Error discovering services!")
            return
        }
        
        guard let services = peripheral.services else {
            return
        }
        
        for service in services {
            peripheral.discoverCharacteristics(nil, for: service)
        }
        print("Discovered Services: \(services)")
        addStatusMessage(message: "Services discovered")
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
        addStatusMessage(message: "Found \(characteristics.count) characteristics.")
        
        for characteristic in characteristics {
            print(characteristic.description)
            
            if characteristic.uuid.isEqual(CBUUIDs.BLECharacteristicUUID) {
                reverseCharacteristic = characteristic
                addStatusMessage(message: "Reverse Characteristic set")
                connected = true
            }
            
            else if characteristic.uuid.isEqual(CBUUIDs.BLENotifyCharacteristicUUID) {
                notifyCharacteristic = characteristic
                addStatusMessage(message: "Notify Characteristic set")
                connected = true
                
                peripheral.setNotifyValue(true, for: notifyCharacteristic)
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
            let newMessage = Message(id: messages.count, msg: "R: \(ASCIIString! as String)")
            messages.append(newMessage)
            print("Value received \(ASCIIString! as String).")
        }
        else if characteristic == notifyCharacteristic {
            let ASCIIString = NSString(data: characteristic.value ?? Data(), encoding: String.Encoding.utf8.rawValue)
            let newMessage = Message(id: messages.count, msg: "R: \(ASCIIString! as String)")
            messages.append(newMessage)
            print("Value received \(ASCIIString! as String).")
        }
    }
    
    func peripheral(_ peripheral: CBPeripheral, didModifyServices invalidatedServices: [CBService]) {
        connected = false
        startScanning()
    }
    
    /// Appends a message to the status messages array
    /// - Parameter msg: a String describing the message
    private func addStatusMessage(message msg: String) {
        let newStatus = StatusMsg(id: statusMsgs.count, msg: msg)
        statusMsgs.append(newStatus)
        print(msg)
    }
    
    func toggleNotifyCharacteristic(enabled e: Bool) {
        myPeripheral.setNotifyValue(e, for: notifyCharacteristic)
    }
}
