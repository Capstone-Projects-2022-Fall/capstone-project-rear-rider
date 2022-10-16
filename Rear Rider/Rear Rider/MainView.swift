// RearRider
//
// Calin Pescaru
//
// October 2022
//
// A simple TabView that one can use to navigate around the app

import SwiftUI

struct MainView: View {
    @EnvironmentObject var bleManager: BLEManager
    
    var body: some View {
        VStack {
            HStack {
                Button {
                    bleManager.startScanning()
                } label: {
                    if bleManager.connected {
                        Image(systemName: "b.circle")
                            .foregroundColor(.green)
                    }
                    else {
                        Image(systemName: "b.circle")
                            .foregroundColor(.red)
                    }
                }

                Image(systemName: "wifi.circle")
                    .foregroundColor(.green)
            }
            
            TabView {
                RiderView()
                    .tabItem {
                        Image(systemName: "bicycle")
                    }
                CameraTestView()
                    .tabItem {
                        Image(systemName: "camera")
                    }
                BluetoothView()
                    .tabItem {
                        Image(systemName: "wrench.and.screwdriver")
                    }
            }
        }
    }
}

struct MainView_Previews: PreviewProvider {
    static var previews: some View {
        MainView()
    }
}
