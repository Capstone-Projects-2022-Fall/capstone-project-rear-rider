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
}

class ImageIdentification: ObservableObject {
    private var visionModel: VNCoreMLModel!
    private var bndRects = [BoundingRect]() {
        didSet {
            DispatchQueue.main.async {
                self.bndRectsCopy = self.bndRects // fix for Publishing from Background Thread purple warning
            }
        }
    }
    @Published var bndRectsCopy = [BoundingRect]()
    
    init() {
        self.visionModel = initVisionModel()
    }
    
    func initVisionModel() -> VNCoreMLModel {
        do {
            let model = try? yolov5m(configuration: MLModelConfiguration()).model
            return try VNCoreMLModel(for: model!)
        } catch {
            fatalError("Failed to create Vsion model: \(error).")
        }
    }
    
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
                        // 389x219 is the size of the Image and ZStack views in CameraTestView with scaledToFit property
                        self.bndRects.append(BoundingRect(id: self.bndRects.count, rect: VNImageRectForNormalizedRect(temp, 389, 288)))
                        
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
    
    func clearBndRects() {
        self.bndRects.removeAll()
        self.bndRectsCopy.removeAll()
    }
}
