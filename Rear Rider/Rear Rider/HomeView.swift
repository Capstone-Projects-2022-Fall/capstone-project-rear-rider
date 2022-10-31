//
//  HomeView.swift
//  Rear Rider
//
//  Created by Bobby Palko on 9/28/22.
//

import SwiftUI

struct HomeView: View {
    @EnvironmentObject var bleManager: BLEManager
    @EnvironmentObject var wifiManager: WifiManager
    
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

                if wifiManager.wifiOn {
                    Image(systemName: "wifi.circle")
                        .foregroundColor(.green)
                }
                else {
                    Image(systemName: "wifi.circle")
                        .foregroundColor(.red)
                }
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
                OptionsView()
                    .tabItem {
                        Image(systemName: "gear")
                    }
            }
        }
    }
}

struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView().environmentObject(BLEManager())
            .environmentObject(WifiManager())
    }
}
