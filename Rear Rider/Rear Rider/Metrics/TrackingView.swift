//
//  TrackingView.swift
//  Rear Rider
//
//  Created by Paul Sutton on 11/30/22.
//

import SwiftUI

struct TrackingView: View {
    @EnvironmentObject var trackingManager: TrackingManager
    var body: some View {
        VStack {
            if (trackingManager.mode == .started) {
                Text("\(String(format: "%.2f", trackingManager.lastSeenLocation?.speed ?? 0)) m/s")
                    .fontWeight(.bold)
                    .monospacedDigit()
            } else {
                Text("-/-")
            }
            Text(String(format: "%.1f", trackingManager.secondsElapsed))
                            .font(.custom("Avenir", size: 40))
                            .padding(.top, 200)
                            .padding(.bottom, 100).monospacedDigit()
                        if trackingManager.mode == .stopped {
                            Button(action: {
                                self.trackingManager.start()
                            }) {
                                Text("Start")
                            }
                        }
                        if trackingManager.mode == .started {
                            Button(action: {
                                self.trackingManager.pause()
                            }) {
                                Text("Pause")
                            }
                        }
                        if trackingManager.mode == .paused {
                            Button(action: {
                                self.trackingManager.start()
                            }) {
                                Text("Start")
                            }
                            Button(action: {
                                self.trackingManager.stop()
                            }) {
                                Text("Stop")
                            }
                                .padding(.top, 30)
                        }
        }.navigationTitle("Tracking")
    }
}

struct TrackingView_Previews: PreviewProvider {
    static var previews: some View {
        TrackingView()
    }
}
