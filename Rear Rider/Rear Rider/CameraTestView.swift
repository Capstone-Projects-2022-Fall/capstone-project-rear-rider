// RearRider
//
// Calin Pescaru
//
// October 2022
//
// Present the streaming content.

import SwiftUI
import AVKit

struct CameraTestView: View {
    @ObservedObject private var stream = MjpegStreamingController()
    @State private var playing = true
    @State private var mlResult = ""
    
    var body: some View {
        VStack {
            Image(uiImage: stream.uiImage)
            
            Spacer()
            
            Text(mlResult)
            
            HStack(spacing: 100) {
                Button(action: {
                    stream.play()
                    playing = true
                }) {
                    Text("Play")
                }.disabled(playing)
                
                Button(action: {
                    stream.stop()
                    playing = false
                }) {
                    Text("Stop")
                }.disabled(!playing)
                
                Button(action: {
                    mlResult = stream.classify(image: stream.uiImage)
                }) {
                    Text("Classify")
                }
            }
        }
        .onAppear() {
            stream.play()
        }
    }
}

struct CameraTest_Previews: PreviewProvider {
    static var previews: some View {
        CameraTestView()
    }
}
