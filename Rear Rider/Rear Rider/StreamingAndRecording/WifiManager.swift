// RearRider
//
// Calin Pescaru
//
// October 2022
//
// Bluetooth Manager
//
// Manages the Wi-Fi connection with the RPi.

import Foundation

/// Handles the Wi-Fi connection with the RPi. The commands are sent over BT
class WifiManager: ObservableObject {
    static var shared = WifiManager()
    private var bleManager = BLEManager.shared
    
    @Published var wifiOn = false
    
    /// Instruct the Pi to turn on its Wi-Fi
    func turnWifiOn() {
        bleManager.turnWifiOn()
        RearRiderLog.shared.addLog(from: "WiFi", message: "Command to turn Wi-Fi on sent")
    }
    
    /// Instruct the Pi to turn off its Wi-Fi
    func turnWifiOff() {
        bleManager.turnWifiOff()
        RearRiderLog.shared.addLog(from: "WiFi", message: "Command to turn Wi-Fi off sent")
    }
    
    func setWifi(isOn on: Bool) { wifiOn = on }
}
