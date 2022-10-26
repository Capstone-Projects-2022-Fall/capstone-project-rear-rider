//
//  HomeView.swift
//  Rear Rider
//
//  Created by Bobby Palko on 9/28/22.
//

import SwiftUI

struct HomeView: View {
    @EnvironmentObject var bleManager: BLEManager
    var alert = RearRiderAlerts()
    
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
            
//            Spacer().padding()
//            
//            Button {
//                try! alert.loadSoundFile(fileName: "vehicleAlert")
//                alert.playAudioAlert()
//            } label: {
//                Text("Honk")
//            }.padding()
            
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
                OptionsView()
                    .tabItem {
                        Image(systemName:
                                "gear")
                    }
            }
        }
    }
}

struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView()
    }
}
