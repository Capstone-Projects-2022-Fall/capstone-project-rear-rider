// RearRider
//
// Calin Pescaru
//
// December 2022
//
// ObjectIdentification Unit Test
//
// This test requries modifications which are not present in the main branch!

import XCTest
@testable import Rear_Rider

final class ObjectIdentificationTest: XCTestCase {
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
    
    func testDetectFace() throws {
        let model = ImageIdentification.shared
        
        // give enough time to connect to the Pi's Wi-Fi
        result = XCTWaiter.wait(for: [XCTestExpectation()], timeout: 7)
        
        // you have 7 seconds to point the camera at your face
        result = XCTWaiter.wait(for: [XCTestExpectation()], timeout: 7)
        
        var person: String = ""
        for obj in model.bndRects {
            if obj.object == "person" {
                person = "person"
                break
            }
        }
            
        XCTAssertEqual(person, "person")
    }
}
