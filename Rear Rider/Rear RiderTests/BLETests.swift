//
//  BLETests.swift
//  BleTutorialTests
//
//  Created by Lydia Pescaru on 10/26/22.
//

import XCTest
@testable import BleTutorial

class BLETests: XCTestCase {
    private var bleManager: BLEManager! = nil

    override func setUpWithError() throws {
        // Put setup code here. This method is called before the invocation of each test method in the class.
        try? super.setUpWithError()
        bleManager = BLEManager()
    }

    override func tearDownWithError() throws {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        
        bleManager.disconnectBLE()
        try? super.tearDownWithError()
    }

    func testConnectionSuccessful() throws {
        //give iPhone enough time to connect to the RPi
        let result = XCTWaiter.wait(for: [XCTestExpectation()], timeout: 5)
        if result == XCTWaiter.Result.timedOut {
            XCTAssert(bleManager.statusMsgs.contains(where: {$0.msg == "Connection successful"}))
        }
    }
}
