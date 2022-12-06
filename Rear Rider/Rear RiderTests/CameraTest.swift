// RearRider
//
// Calin Pescaru
//
// December 2022
//
// Camera Unit Test
//
// This test requries modifications which are not present in the main branch!

import XCTest
@testable import Rear_Rider

class CameraTest: XCTestCase {
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
    
    func testReceivingCameraFeed() throws {
        // give enough time to connect to the Pi's Wi-Fi
        result = XCTWaiter.wait(for: [XCTestExpectation()], timeout: 7)
        let stream = MjpegStreamingController.shared
        
        // The first 2 bytes of a jpeg image are 0xff = 255 and 0xd8 = 216
        let byte1 = UInt8(stream.receivedData?[0] ?? 0)
        let byte2 = UInt8(stream.receivedData?[1] ?? 0)
        
        XCTAssertEqual(byte1, 255)
        XCTAssertEqual(byte2, 216)
    }
}
