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
    
    var body: some Scene {
        WindowGroup {
            MainView()
                .environmentObject(bleManager)
        }
    }
}
