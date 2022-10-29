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
    
    // declare a timer that will call a function every 0.3 seconds
    private let timer = Timer.publish(every: 0.3, on: .main, in: .common)

    var body: some View {
        VStack {
            ZStack {
                ForEach (mLModel.bndRectsCopy) { rect in
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
                
            Button(action: {
                mLModel.clearBndRects()
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
            _ = timer.connect()
        }
        .onReceive(timer) { time in
            mLModel.clearBndRects()
            mLModel.detectObjects(image: stream.uiImage)
        }
    }
}

struct CameraTest_Previews: PreviewProvider {
    static var previews: some View {
        CameraTestView().environmentObject(BLEManager())
    }
}
