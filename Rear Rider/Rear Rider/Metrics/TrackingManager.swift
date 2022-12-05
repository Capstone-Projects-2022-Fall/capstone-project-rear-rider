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
    @Published var currentPlacemark: CLPlacemark?
    @Published var mode: TrackingMode = .stopped
    @Published var locationsArray = [CLLocation]()
    @Published var cummulativeDistance = 0.0
    private var milestone = 0.0
    private var splitDistance = 50.00
    @Published var hours = 0
    @Published var minutes = 0
    @Published var seconds = 0
    private var secondsElapsed = 0
    private var secondsMilestone = 0
    private var splits = [Split]()
    
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
            fetchCountryAndCity(for: locations.first)
        } else {
            lastSeenLocation = locations.first
            guard let dist = locations.first?.distance(from: locationsArray.last!) else{return}
            locationsArray.append(locations.first!)
            cummulativeDistance += dist
            fetchCountryAndCity(for: locations.first)
            if (cummulativeDistance - milestone >= splitDistance) {
                splits.append(Split(seconds: secondsMilestone, distance: splitDistance))
                milestone = cummulativeDistance
                secondsMilestone = 0
                print(splits)
            }
        }
    }
    
    func fetchCountryAndCity(for location: CLLocation?) {
        guard let location = location else { return }
        let geocoder = CLGeocoder()
        geocoder.reverseGeocodeLocation(location) { (placemarks, error) in
            self.currentPlacemark = placemarks?.first
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
        locationsArray.removeAll()
        mode = .stopped
    }
    
    func secondsToHoursMinutesSeconds(_ seconds: Int) -> (Int, Int, Int) {
        return (seconds / 3600, (seconds % 3600) / 60, (seconds % 3600) % 60)
    }
}
