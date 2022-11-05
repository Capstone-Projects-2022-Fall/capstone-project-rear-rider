//
//  ConfigurationOptions.swift
//  Rear RiderTests
//
//  Created by Bobby Palko on 11/5/22.
//

import XCTest
@testable import Rear_Rider

final class ConfigurationOptionsTest: XCTestCase {
        
    var conf: UserConfig!
    var LIGHT_STRING = "rgb(55,55,55)"
        
    override func setUpWithError() throws {
        conf = UserConfig()
        
        conf.audioFile = ConfigOptions.AudioFile.honk.rawValue
        conf.lightPattern = ConfigOptions.LightPattern.strobe.rawValue
        conf.lightBrightness = ConfigOptions.LightBrightness.medium.rawValue
        conf.lightColor = LIGHT_STRING
    }

    override func tearDownWithError() throws {
        // remove any saved config data
        UserDefaults.standard.removeObject(forKey: "RearRiderConfig")
    }
    
    func testSaveNoErrors() {
        var thrownError: Error?
        
        do {
            try conf.save()
        }
        catch let e {
            thrownError = e
        }
        
        XCTAssertNil(thrownError)
    }
    
    func testLoadNoErrors() {
        var thrownError: Error?
        
        // save dummy data
        try! conf.save()
        
        // modify the values of the conf object
        conf.audioFile = ConfigOptions.AudioFile.off.rawValue
        conf.lightPattern = ConfigOptions.LightPattern.off.rawValue
        conf.lightBrightness = ConfigOptions.LightBrightness.low.rawValue
        conf.lightColor = "rgb(3,3,3)"
        
        // load the stored data, overwriting our changes
        do {
            try conf.load()
        }
        catch let e {
            thrownError = e
        }
        
        XCTAssertNil(thrownError)
        
        XCTAssertEqual(conf.audioFile, ConfigOptions.AudioFile.honk.rawValue)
        XCTAssertEqual(conf.lightPattern, ConfigOptions.LightPattern.strobe.rawValue)
        XCTAssertEqual(conf.lightBrightness, ConfigOptions.LightBrightness.medium.rawValue)
        XCTAssertEqual(conf.lightColor, LIGHT_STRING)
    }
    
    func testSaveBadAudioFileThrowsValidationError() {
        var thrownError: Error?
        let expectedError = ConfigErrors.validationError("Unacceptable audio file")
        
        conf.audioFile = "B-B-B-BERRRR" //airhorn sound XD
        
        // verify we throw an error
        XCTAssertThrowsError(try conf.save()) {
            thrownError = $0
        }
        
        XCTAssertEqual(thrownError?.localizedDescription, expectedError.localizedDescription)
    }
    
    func testSaveBadLightPatternThrowsValidationError() {
        var thrownError: Error?
        let expectedError = ConfigErrors.validationError("Unacceptable light pattern value")
        
        conf.lightPattern = -1
        
        // verify we throw an error
        XCTAssertThrowsError(try conf.save()) {
            thrownError = $0
        }
        
        XCTAssertEqual(thrownError?.localizedDescription, expectedError.localizedDescription)
    }
    
    func testSaveBadLightBrightnessThrowsValidationError() {
        var thrownError: Error?
        let expectedError = ConfigErrors.validationError("Unacceptable brightness value")
        
        conf.lightBrightness = -1
        
        // verify we throw an error
        XCTAssertThrowsError(try conf.save()) {
            thrownError = $0
        }
        
        XCTAssertEqual(thrownError?.localizedDescription, expectedError.localizedDescription)
    }
    
    func testLoadNoSaveThrowsLoadError() {
        var thrownError: Error?
        let expectedError = ConfigErrors.loadError("Unacceptable brightness value")
        
        // verify we throw an error
        XCTAssertThrowsError(try conf.load()) {
            thrownError = $0
        }
        
        XCTAssertEqual(thrownError?.localizedDescription, expectedError.localizedDescription)
    }
}
