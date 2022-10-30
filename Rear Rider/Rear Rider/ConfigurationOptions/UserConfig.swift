//
//  UserConfig.swift
//  Rear Rider
//
//  Created by Bobby Palko on 10/25/22.
//

import Foundation
import SwiftUI

/**
 * A Codable object to store our user data that can easily be passed as JSON
 */
struct ConfigData: Codable {
    let audioFile: String
    let lightPattern: Int
    let lightColor: String
    let lightBrightness: Int
}

/**
 * All acceptable configurations
 */
enum ConfigOptions {
    enum AudioFile: String, CaseIterable, Equatable {
        case honk = "vehicleAlert"
        case off = ""
        
        var description: String {
            switch self {
                case .honk:
                    return "Honk"
                case .off:
                    return "None"
            }
        }
    }
    
    enum LightPattern: Int, CaseIterable, Equatable {
        case strobe = 1
        case off = 0
        
        var description: String {
            switch self {
                case .strobe:
                    return "Strobe"
                case .off:
                    return "None"
            }
        }
    }
    
    enum LightBrightness: Int, CaseIterable, Equatable {
        case low = 1
        case medium = 2
        case high = 3
        
        var description: String {
            switch self {
                case .low:
                    return "Low"
                case .medium:
                    return "Medium"
                case .high:
                    return "High"
            }
        }
    }
}

/**
 * Possible Errors that can occur while interacting with the UserConfig
 */
enum ConfigErrors: Error {
    case loadError(String)
    case validationError(String)
}


/**
 * A wrapper class to store and retrieve user configuration options
 */
class UserConfig: ObservableObject {
    let defaults = UserDefaults.standard
    
    // default values. get overwritten on successful load
    var audioFile: String = ConfigOptions.AudioFile.honk.rawValue
    var lightPattern: Int = ConfigOptions.LightPattern.strobe.rawValue
    var lightColor: String = "rgb(255,255,255)"
    var lightBrightness: Int = 1
    
    var lColor: Color = Color.white
    
    private let bleManager = BLEManager.shared
    private let log = RearRiderLog.shared

    init() {
        do {
            try load()
        } catch {
            // load fails on init, just use defaults
        }
    }

    /**
     * Loads the saved configuration object
     * @throws loadError if the configuration does not exist or if there was a problem decoding it
     */
    func load() throws {
        if let encodedData = defaults.object(forKey: "RearRiderConfig") as? Data {
            let decoder = JSONDecoder()
            if let savedData = try? decoder.decode(ConfigData.self, from: encodedData) {
                // TODO make this a loop
                self.audioFile = savedData.audioFile
                self.lightPattern = savedData.lightPattern
                self.lightColor = savedData.lightColor
                self.lightBrightness = savedData.lightBrightness
                
                print("LOADED: \(savedData)")
                log.addLog(from: "UserConfig", message: "Loaded configuration")
            } else {
                log.addLog(from: "UserConfig", message: "Error decoding RearRiderConfig Data!")
                throw ConfigErrors.loadError("Error decoding RearRiderConfig Data!")
            }
        } else {
            log.addLog(from: "UserConfig", message: "RearRiderConfig not present!")
            throw ConfigErrors.loadError("RearRiderConfig not present")
        }
    }
    
    /**
     * Saves the current config
     * @throws validationError when validation fails
     */
    func save() throws {
        do {
            try validate()
        } catch let error {
            throw error
        }

        // any way to dynamically add these?
        let data = ConfigData(
            audioFile: audioFile,
            lightPattern: lightPattern,
            lightColor: lightColor,
            lightBrightness: lightBrightness
        )
        let encoder = JSONEncoder()
        if let encodedData = try? encoder.encode(data) {
            defaults.set(encodedData, forKey: "RearRiderConfig")
            print("SAVED: \(data)")
            log.addLog(from: "UserConfig", message: "Saved configuration")
        }
        
        /* Prepare data to be sent over BT
         * The format is as follows:
         * 1st byte - light brightness
         * 2nd byte - light pattern
         * 3rd byte - red value
         * 4th byte - green value
         * 5th byte - blue value
         */
        var bytes = Data()
        var br: UInt8 = UInt8(lightBrightness)
        var pat: UInt8 = UInt8(lightPattern)
        let rgb: [Int] = Color.fromStringToInt(color: lColor.description)
        var red: UInt8 = UInt8(rgb[0])
        var green: UInt8 = UInt8(rgb[1])
        var blue: UInt8 = UInt8(rgb[2])
        
        bytes.append(withUnsafeBytes(of: &br) { Data($0) })
        bytes.append(withUnsafeBytes(of: &pat) { Data($0) })
        bytes.append(withUnsafeBytes(of: &red) { Data($0) })
        bytes.append(withUnsafeBytes(of: &green) { Data($0) })
        bytes.append(withUnsafeBytes(of: &blue) { Data($0) })
        bleManager.sendConfigToPi(data: bytes)
    }
    
    /**
     * Validates the current config is part of the predetermined options
     * @throws validationError if the current config is not in an acceptable state
     */
    func validate() throws {
        if !ConfigOptions.AudioFile.allCases.contains(where: {$0.rawValue == self.audioFile}) {
            log.addLog(from: "UserConfig", message: "Unacceptable audio file")
            throw ConfigErrors.validationError("Unacceptable audio file")
        }
        if !ConfigOptions.LightPattern.allCases.contains(where: {$0.rawValue == self.lightPattern}) {
            log.addLog(from: "UserConfig", message: "Unacceptable light pattern value")
            throw ConfigErrors.validationError("Unacceptable light pattern value")
        }
        if !ConfigOptions.LightBrightness.allCases.contains(where: {$0.rawValue == self.lightBrightness}) {
            log.addLog(from: "UserConfig", message: "Unacceptable brightness value")
            throw ConfigErrors.validationError("Unacceptable brightness value")
        }
    }
}
