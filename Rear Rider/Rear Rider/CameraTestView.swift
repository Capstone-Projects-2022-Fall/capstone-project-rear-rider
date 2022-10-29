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
    @ObservedObject private var mLModel = ImageIdentification()
    @State private var index = 1

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
                
                Image(uiImage: mLModel.resizeImg(image: UIImage(imageLiteralResourceName: "\(index)")))
                    .resizable()
                    .scaledToFit()
            }
            .scaledToFit()
            
            //RecordingView()
                
            HStack {
                Button(action: {
                    mLModel.detectObject(image: UIImage(imageLiteralResourceName: "\(index)"))
                }) {
                    Text("Classify")
                }
                
                Button(action: {
                    mLModel.clearBndRects()
                    if index == 13 {
                        index = 1
                    } else {
                        index += 1
                    }
                }) {
                    Text("Next")
                }
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
