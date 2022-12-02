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

    @StateObject var mLModel = ImageIdentification.shared
    @StateObject var viewRouter = ViewRouter()
    @StateObject var bleManager = BLEManager.shared
    @StateObject var conf = UserConfig()
    @StateObject var log = RearRiderLog.shared
    @StateObject var wifiManager = WifiManager.shared
    @StateObject var alert = RearRiderAlerts.shared
    @StateObject var auth = AuthModel()
    @StateObject var db = FirestoreModel()
    
    var body: some Scene {
        WindowGroup {
            ViewController()
                .environmentObject(bleManager)
                .environmentObject(log)
                .environmentObject(conf)
                .environmentObject(wifiManager)
                .environmentObject(alert)
                .environmentObject(viewRouter)
                .environmentObject(auth)
                .environmentObject(db)
        }
    }
}
