//
//  HomeView.swift
//  Rear Rider
//
//  Created by Bobby Palko on 9/28/22.
//

import SwiftUI

struct HomeView: View {
    var body: some View {
        NavigationView {
            VStack {
                NavigationLink(destination: ObjectDetectionView()) {
                    Text("Machine Learning Demo")
                }

                NavigationLink(destination: BluetoothView()) {
                    Text("Bluetooth Connection Demo")
                }
                
                NavigationLink(destination: CameraTestView()) {
                    Text("Stream")
                }
                 
            }.navigationBarTitle("Rear Rider", displayMode: .inline)
        }
    }
}

struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView()
    }
}
