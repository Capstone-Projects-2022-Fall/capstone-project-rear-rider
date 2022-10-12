//
//  ImageIdentification.swift
//  Rear Rider
//
//  Created by Bobby Palko on 10/11/22.
//

import CoreML
import UIKit

struct ImageIdentification {
    
    let model = try? MobileNetV2(configuration: MLModelConfiguration())
    
    func classify(image img: UIImage) -> String {
        let resizedImage = img.resizeImageTo(size: CGSize(width: 224, height: 224))
        let buffer = resizedImage!.convertToBuffer()
        
        let output = try? model!.prediction(image: buffer!)
        
        if let output = output {
            let results = output.classLabelProbs.sorted { $0.1 > $1.1 }
            let result = results.map { (key, value) in
                return "\(key) = \(String(format: "%.2f", value * 100))%"
            }.joined(separator: "\n")
            
            return result
        }
        
        return ""
    }
}
