//
//  LocationManager.swift
//  Rear Rider
//
//  Created by Paul Sutton on 11/30/22.
//

import Foundation
import CoreLocation

class TrackingManager: NSObject, ObservableObject, CLLocationManagerDelegate {
    @Published var authorizationStatus: CLAuthorizationStatus
    @Published var lastSeenLocation: CLLocation?
    @Published var mode: TrackingMode = .stopped
    @Published var locationsArray = [CLLocation]()
    @Published var cummulativeDistance = 0.0
    @Published var hours = 0
    @Published var minutes = 0
    @Published var seconds = 0
    @Published var secondsElapsed = 0
    private var milestone = 0.0
    private var secondsMilestone = 0
    @Published var splits = [Split]()
    private var splitDistance = 50.00
    
    private var timer = Timer()
    
    private let locationManager: CLLocationManager
    
    override init() {
        locationManager = CLLocationManager()
        authorizationStatus = locationManager.authorizationStatus
        
        super.init()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
        locationManager.distanceFilter = kCLDistanceFilterNone
        locationManager.allowsBackgroundLocationUpdates = true
        locationManager.showsBackgroundLocationIndicator = true
    }
    
    
    enum TrackingMode {
        case started
        case stopped
        case paused
    }
    
    func requestPermission() {
        locationManager.requestWhenInUseAuthorization()
    }
    
    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        authorizationStatus = manager.authorizationStatus
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        if (locationsArray.isEmpty) {
            locationsArray.append(locations.first!)
            lastSeenLocation = locations.first
            guard let dist = locations.first?.distance(from: locationsArray.last!) else{return}
            cummulativeDistance += dist
        } else {
            lastSeenLocation = locations.first
            guard let dist = locations.first?.distance(from: locationsArray.last!) else{return}
            locationsArray.append(locations.first!)
            cummulativeDistance += dist
            if (cummulativeDistance - milestone >= splitDistance) {
                splits.append(Split(seconds: secondsMilestone, distance: splitDistance))
                milestone = cummulativeDistance
                secondsMilestone = 0
            }
        }
    }
    
    func start() {
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { timer in
            self.secondsElapsed = self.secondsElapsed + 1
            self.secondsMilestone = self.secondsMilestone + 1
            let (h,m,s) = self.secondsToHoursMinutesSeconds(self.secondsElapsed)
            self.hours = h
            self.minutes = m
            self.seconds = s
        }
        locationManager.startUpdatingLocation()
        mode = .started
    }
    
    func pause() {
        locationManager.stopUpdatingLocation()
        timer.invalidate()
        mode = .paused
    }
        
    func stop() {
        locationManager.stopUpdatingLocation()
        timer.invalidate()
        secondsElapsed = 0
        seconds = 0
        minutes = 0
        hours = 0
        cummulativeDistance = 0.0
        milestone = 0.0
        secondsMilestone = 0
        locationsArray.removeAll()
        splits.removeAll()
        lastSeenLocation = nil
        mode = .stopped
    }
    
    func secondsToHoursMinutesSeconds(_ seconds: Int) -> (Int, Int, Int) {
        return (seconds / 3600, (seconds % 3600) / 60, (seconds % 3600) % 60)
    }
}
