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
    @ObservedObject private var stream = MjpegStreamingController(url: "http://10.42.0.1:8000/stream.mjpg")
    @State private var playing = true
    @State private var mlResult = ""
    private var mLModel = ImageIdentification()

    var body: some View {
        VStack {
            Image(uiImage: stream.uiImage)
            
            RecordingView()
            
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
                    self.mlResult = mLModel.classify(image: stream.uiImage)
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
