//
//  Rear_RiderApp.swift
//  Rear Rider
//
//  Created by Bobby Palko on 9/28/22.
//

import SwiftUI
import UIKit
import FirebaseCore

class AppDelegate: NSObject, UIApplicationDelegate {

  func application(_ application: UIApplication,
                   didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]? = nil) -> Bool {
    FirebaseApp.configure()

    return true
  }
}


@main
struct Rear_RiderApp: App {
    // register app delegate for Firebase setup
    @UIApplicationDelegateAdaptor(AppDelegate.self) var delegate

    @StateObject var bleManager = BLEManager.shared
    @StateObject var conf = UserConfig()
    @StateObject var log = RearRiderLog.shared
    @StateObject var wifiManager = WifiManager.shared
    
    var body: some Scene {
        WindowGroup {
            HomeView()
                .environmentObject(bleManager)
                .environmentObject(log)
                .environmentObject(conf)
                .environmentObject(wifiManager)
        }
    }
}
