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
    @EnvironmentObject var wifiManager: WifiManager
    @ObservedObject private var stream = MjpegStreamingController(url: "http://raspberrypi.local:8000/stream.mjpg")
    private var mLModel = ImageIdentification()
    
    // declare a timer that will call a function every 0.3 seconds
    private let timer = Timer.publish(every: 0.3, on: .main, in: .common)
    @State var timer_set = false

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
                
                if wifiManager.wifiOn {
                    Image(uiImage: stream.uiImage)
                        .resizable()
                        .scaledToFit()
                }
                else {
                    Text("Waiting for Wi-Fi to connect...")
                }
            }
            .scaledToFit()
            
            RecordingView()
            
            HStack {
                Button(action: {
                    if wifiManager.wifiOn {
                        stream.play()
                        if !timer_set {
                            _ = timer.connect()
                            timer_set = true
                        }
                    }
                }) {
                    Text("Play")
                }
                
                Spacer()
                
                Button(action: {
                    mLModel.clearBndRects()
                    mLModel.detectObjects(image: stream.uiImage)
                }) {
                    Text("Classify")
                }
            }
        }
        .onAppear() {
            if (bleManager.connected) {
                bleManager.toggleNotifyCharacteristic(enabled: false)
                wifiManager.turnWifiOn()
            }
        }
        .onReceive(timer) { time in
            if wifiManager.wifiOn {
                mLModel.clearBndRects()
                mLModel.detectObjects(image: stream.uiImage)
            }
        }
        .onDisappear() {
            if (wifiManager.wifiOn) {
                wifiManager.turnWifiOff()
                timer.connect().cancel()
                timer_set = false
            }
        }
    }
}

struct CameraTest_Previews: PreviewProvider {
    static var previews: some View {
        CameraTestView().environmentObject(BLEManager())
    }
}
