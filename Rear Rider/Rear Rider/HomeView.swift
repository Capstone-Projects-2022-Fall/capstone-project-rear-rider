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
                
//                  Uncomment once BT view is in project
//
//                NavigationLink(destination: BTConnectionView()) {
//                    Text("Bluetooth Connection Demo")
//                }
                 
            }.navigationBarTitle("Rear Rider", displayMode: .inline)
        }
    }
}

struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView()
    }
}
