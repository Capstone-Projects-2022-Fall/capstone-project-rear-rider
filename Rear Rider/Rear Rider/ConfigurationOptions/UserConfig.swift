//
//  UserConfig.swift
//  Rear Rider
//
//  Created by Bobby Palko on 10/25/22.
//

import Foundation

/**
 * A Codable object to store our user data that can easily be passed as JSON
 */
struct ConfigData: Codable {
    let audioFile: String
    let lightPattern: String
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

    enum LightPattern: String, CaseIterable, Equatable {
        case strobe = "strobe"
        case off = ""
        
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
    var lightPattern: String = ConfigOptions.LightPattern.strobe.rawValue
    var lightColor: String = ""
    var lightBrightness: Int = 1

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
            } else {
                throw ConfigErrors.loadError("Error decoding RearRiderConfig Data!")
            }
        } else {
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
            // TODO send the conf to the device
        }
        
    }
    
    /**
     * Validates the current config is part of the predetermined options
     * @throws validationError if the current config is not in an acceptable state
     */
    func validate() throws {
        if !ConfigOptions.AudioFile.allCases.contains(where: {$0.rawValue == self.audioFile}) {
            throw ConfigErrors.validationError("Unacceptable audio file")
        }
        if !ConfigOptions.LightPattern.allCases.contains(where: {$0.rawValue == self.lightPattern}) {
            throw ConfigErrors.validationError("Unacceptable light pattern value")
        }
        if !ConfigOptions.LightBrightness.allCases.contains(where: {$0.rawValue == self.lightBrightness}) {
            throw ConfigErrors.validationError("Unacceptable brightness value")
        }
    }
}
