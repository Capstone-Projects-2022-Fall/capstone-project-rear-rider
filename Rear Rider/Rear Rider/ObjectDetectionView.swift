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
    let photos = ["bike","Car","person"]
    @State private var currentIndex: Int = 0
    @State private var classificationLabel: String = ""
    private var mLModel = ImageIdentification()
    
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
        
        guard let image = UIImage(named: currentImageName) else { return }
        
        self.classificationLabel = mLModel.classify(image: image)
    }
}

struct ObjectDetectionView_Previews: PreviewProvider {
    static var previews: some View {
        ObjectDetectionView()
    }
}
