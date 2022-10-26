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
    @EnvironmentObject var bleManager: BLEManager
    @ObservedObject private var stream = MjpegStreamingController(url: "http://10.42.0.1:8000/stream.mjpg")
    @State private var playing = true
    @State private var mlResult = ""
    private var mLModel = ImageIdentification()

    var body: some View {
        VStack {
            Image(uiImage: stream.uiImage)
                .resizable()
                .frame(width: 640, height: 480)
            
            RecordingView()
            
            Spacer()
            
            Text(mlResult)
                
            Button(action: {
                self.mlResult = mLModel.classify(image: stream.uiImage)
            }) {
                Text("Classify")
            }
        }
        .onAppear() {
            if (bleManager.connected) {
                bleManager.toggleNotifyCharacteristic(enabled: false)
            }
            stream.play()
        }
    }
}

struct CameraTest_Previews: PreviewProvider {
    static var previews: some View {
        CameraTestView()
    }
}
