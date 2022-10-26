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
    private var mLModel = ImageIdentification()

    var body: some View {
        VStack {
            ZStack {
                ForEach (mLModel.bndRects) { rect in
                    Rectangle()
                        .frame(width: rect.rect.width, height: rect.rect.height)
                        .border(.yellow, width: 1)
                        .zIndex(20)
                        .foregroundColor(.clear)
                        .position(x: rect.rect.minX + rect.rect.width / 2, y: rect.rect.minY - rect.rect.height / 2)
                }
                
                Image(uiImage: stream.uiImage)
                    .resizable()
                    .scaledToFit()
            }
            .scaledToFit()
            
            RecordingView()
            
            //Spacer()
                
            Button(action: {
                mLModel.bndRects.removeAll()
                mLModel.detectObjects(image: stream.uiImage)
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
        CameraTestView().environmentObject(BLEManager())
    }
}
