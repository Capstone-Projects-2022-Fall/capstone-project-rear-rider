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
                    Image(systemName: "b.circle")
                        .foregroundColor(bleManager.connected ? .green : .red)
                }

                Image(systemName: "wifi.circle")
                    .foregroundColor(wifiManager.wifiOn ? .green : .red)
            }
            TabView {
                CameraTestView()
                    .tabItem {
                        Image(systemName: "bicycle")
                    }
                ActiveView()
                    .tabItem {
                    Image(systemName: "location")
                }
                
                RideHistoryView()
                    .tabItem {
                        Image(systemName: "chart.bar.xaxis")
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
