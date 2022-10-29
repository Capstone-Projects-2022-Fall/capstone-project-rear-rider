//
//  Rear_RiderApp.swift
//  Rear Rider
//
//  Created by Bobby Palko on 9/28/22.
//

import SwiftUI
import UIKit

@main
struct Rear_RiderApp: App {
    @StateObject var bleManager = BLEManager()
    @StateObject var conf = UserConfig()
    
    var body: some Scene {
        WindowGroup {
            HomeView()
                .environmentObject(bleManager)
        }
    }
}
