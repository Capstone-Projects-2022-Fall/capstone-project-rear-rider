//
//  TrackingManager.swift
//  Rear Rider
//
//  Created by Paul Sutton on 12/1/22.
//

import Foundation

class TrackingManger: ObservableObject {
    
    enum TrackingMode {
        case started
        case stopped
        case paused
    }
    
    @Published var secondsElapsed = 0.0
    @Published var mode: TrackingMode = .stopped
    
    var timer = Timer()
    var locationManger = LocationManager()
    
    func start() {
        locationManger.startTracking()
        timer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { timer in
            self.secondsElapsed = self.secondsElapsed + 0.1
        }
        mode = .started
    }
    
    func pause() {
        locationManger.stopTracking()
        timer.invalidate()
        mode = .paused
    }
        
    func stop() {
        locationManger.stopTracking()
        timer.invalidate()
        secondsElapsed = 0
        mode = .stopped
    }
    
}
