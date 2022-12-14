// RearRider
//
// Calin Pescaru
//
// October 2022
//
// Identify objects using the YOLOv3 model.

import Foundation
import UIKit
import CoreML
import Vision

struct BoundingRect: Identifiable {
    var id: Int
    var rect: CGRect
    var object: String
    var confidence: Float
}

/// A class for detecting object using a Core ML model
class ImageIdentification: ObservableObject {
    static var shared = ImageIdentification()
    private var visionModel: VNCoreMLModel!
    var bndRects = [BoundingRect]()
    private var locked: Bool = false
    
    init() {
        self.visionModel = initVisionModel()
    }
    
    /// Initializes a VNCoreMLModel from a Yolov5 model
    /// - Returns: a VNCoreMLModel object
    func initVisionModel() -> VNCoreMLModel {
        do {
            let model = try? yolov5m(configuration: MLModelConfiguration()).model
            return try VNCoreMLModel(for: model!)
        } catch {
            fatalError("Failed to create Vsion model: \(error).")
        }
    }
    
    /// The workhorse of the detection process
    /// - Returns: a VNCoreMLRequest object
    func visionRequest() -> VNCoreMLRequest {
        let requestCompletionHandler: VNRequestCompletionHandler = { request, error in
            if let results = request.results as? [VNRecognizedObjectObservation] {
                let detectionConfidenceThreshold: Float = 0.6
                for result in results {
                    let resultDetectionConfidence = result.labels.first?.confidence ?? 0
                    if resultDetectionConfidence >= detectionConfidenceThreshold {
                        let detectedObject = result.labels.first?.identifier ?? "Nothing"
                        let detectedObjectConfidence = result.labels.first?.confidence ?? 0
                        
                        let temp = CGRect(x: result.boundingBox.origin.x, y: 1 - result.boundingBox.origin.y, width: result.boundingBox.width, height: result.boundingBox.height)
                        // 389x288 is the size of the Image and ZStack views in CameraTestView with scaledToFit property
                        if !self.locked {
                            self.bndRects.append(BoundingRect(id: self.bndRects.count, rect: VNImageRectForNormalizedRect(temp, 389, 288), object: detectedObject, confidence: detectedObjectConfidence))
                        }
                        
                        print("\(detectedObject) detected with \(detectedObjectConfidence) confidence")
                    }
                }
            } else {
                print("Error while getting the request results.")
            }
        }

        let request = VNCoreMLRequest(model: self.visionModel, completionHandler: requestCompletionHandler)
        request.imageCropAndScaleOption = .scaleFill

        return request
    }
    
    /// This is where image detection starts
    /// - Parameter img: a UIImage object
    func detectObjects(image img: UIImage) {
        // process prediction in background
        DispatchQueue.global().async {
            let resizedImage = img.resizeImageTo(size: CGSize(width: 416, height: 416))
            let buffer = resizedImage?.convertToBuffer()

            let handler = VNImageRequestHandler(cvPixelBuffer: buffer!)

            do {
                try handler.perform([self.visionRequest()])
            } catch {
                print("Failed to perform the Vision request \(error).")
            }
        }
    }
    
    /// Clear all bouding rects
    func clearBndRects() {
        self.bndRects.removeAll()
    }
    
    /// Check the labels of the detected object and compare it them with the allowed ones
    /// - Returns: true or false
    func checkForVehicles() -> Bool {
        let labels: [String] = ["person", "bicycle", "car", "motorcycle", "bus", "truck"]
        locked = true
        
        for obj in bndRects {
            if labels.contains(obj.object) {
                locked = false
                return true
            }
        }
        
        locked = false
        return false
    }
}
