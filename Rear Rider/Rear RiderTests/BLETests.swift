// RearRider
//
// Calin Pescaru
//
// October 2022
//
// Bluetooth Unit Tests


import XCTest
@testable import Rear_Rider

class BLETests: XCTestCase {
    private var bleManager: BLEManager! = nil
    var result: XCTWaiter.Result!

    override func setUpWithError() throws {
        // Put setup code here. This method is called before the invocation of each test method in the class.
        try? super.setUpWithError()
        bleManager = BLEManager()
        //give iPhone enough time to connect to the RPi
        result = XCTWaiter.wait(for: [XCTestExpectation()], timeout: 3)
    }

    override func tearDownWithError() throws {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        bleManager.disconnectBLE()
        try? super.tearDownWithError()
    }

    func testConnectionSuccessful() throws {
        if result == XCTWaiter.Result.timedOut {
            XCTAssert(bleManager.connected)
        }
    }
    
    func testConfigCharacteristicSet() throws {
        if result == XCTWaiter.Result.timedOut {
            XCTAssertNotNil(bleManager.ConfigCharacteristic)
        }
    }
    
    func testWifiCharacteristicSet() throws {
        if result == XCTWaiter.Result.timedOut {
            XCTAssertNotNil(bleManager.WiFiCharacteristic)
        }
    }
    
    func testBTDisconnected() throws {
        if result == XCTWaiter.Result.timedOut {
            bleManager.disconnectBLE()
            XCTAssertFalse(bleManager.connected)
        }
    }
    
    func testWifiTurnsOn() throws {
        if result == XCTWaiter.Result.timedOut {
            bleManager.turnWifiOn()
            let r = XCTWaiter.wait(for: [XCTestExpectation()], timeout: 3) // wait for Wi-Fi to update
            if r == XCTWaiter.Result.timedOut {
                XCTAssertTrue(WifiManager.shared.wifiOn)
            }
        }
    }
}
