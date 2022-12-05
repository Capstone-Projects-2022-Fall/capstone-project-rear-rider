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
        
        var max_area: CGFloat = 0.0
        var index = 0
        var i = 0
        
        // get the max area of the bounding boxes which should be your face
        while i < model.bndRects.count {
            let area = model.bndRects[i].rect.minX * model.bndRects[i].rect.minY
            if area > max_area {
                max_area = area
                index = i
            }
            i += 1
        }
        
        XCTAssertEqual(model.bndRects[index].object, "person")
    }
}
