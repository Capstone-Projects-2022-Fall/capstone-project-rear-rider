//
//  ObjectDetectionView.swift
//  Rear Rider
//
//  Created by Bobby Palko on 9/28/22.
//

import CoreML
import SwiftUI
import Vision

struct ObjectDetectionView: View {
    let model = MobileNetV2()
    let photos = ["bike","Car","person"]
    @State private var currentIndex: Int = 0
    @State private var classificationLabel: String = ""
    
    var body: some View {
        
        VStack {
            Image(photos[currentIndex])
                .resizable()
                .scaledToFit()
                .padding()
            HStack {
                Button("Back") {
                    if currentIndex == 0 {
                        currentIndex = (photos.count - 1)
                    } else {
                        currentIndex -= 1
                    }
                }
                    .padding()
                Button("Next") {
                    if currentIndex >= (photos.count - 1) {
                        currentIndex = 0
                    } else {
                        currentIndex += 1
                    }
                }
                    .padding()
            }
            Button("Classify"){
                classifyImage()
            }
            .padding()
            Text(classificationLabel)
            Spacer()
        }
    }
    
    private func classifyImage() {
        let currentImageName = photos[currentIndex]
        
        guard let image = UIImage(named: currentImageName),
            let resizedImage = image.resizeImageTo(size: CGSize(width: 224, height: 224)),
            let buffer = resizedImage.convertToBuffer() else {
                return
            }
        
        let output = try? model.prediction(image: buffer)
        
        if let output = output {
            let results = output.classLabelProbs.sorted { $0.1 > $1.1 }
            let result = results.map { (key, value) in
                return "\(key) = \(String(format: "%.2f", value * 100))%"
            }.joined(separator: "\n")
            
            self.classificationLabel = result
        }
    }
}

struct ObjectDetectionView_Previews: PreviewProvider {
    static var previews: some View {
        ObjectDetectionView()
    }
}
