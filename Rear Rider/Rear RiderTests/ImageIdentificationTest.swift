//
//  ImageIdentificationTest.swift
//  Rear RiderTests
//
//  Created by Bobby Palko on 10/11/22.
//

import XCTest
@testable import Rear_Rider

final class ImageIdentificationTest: XCTestCase {

    var photos: [String]!
    var mLModel: ImageIdentification!
    
    override func setUpWithError() throws {
        photos = ["bike","Car","person"]
        mLModel = ImageIdentification()
    }

    override func tearDownWithError() throws {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
    }

    func testIdentifyCar() throws {
        // This is an example of a functional test case.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
        // Any test you write for XCTest can be annotated as throws and async.
        // Mark your test throws to produce an unexpected failure when your test encounters an uncaught error.
        // Mark your test async to allow awaiting for asynchronous code to complete. Check the results with assertions afterwards.
        let minivan = photos[1]
        
        guard let image = UIImage(named: minivan) else { return }
        
        let result = mLModel.classify(image: image)
        
        XCTAssert(result.starts(with: "minivan"))
    }

    func testPerformanceExample() throws {
        // This is an example of a performance test case.
        self.measure {
            // Put the code you want to measure the time of here.
        }
    }

}
