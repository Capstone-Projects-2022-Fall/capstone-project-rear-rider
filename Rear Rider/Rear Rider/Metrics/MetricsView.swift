//
//  MetricsView.swift
//  Rear Rider
//
//  Created by Paul Sutton on 11/9/22.
//

import SwiftUI
import Charts

struct MetricsView: View {
    @State var cumDist = 0
    @State var formattedSplits = [FormattedSplit]()
    @State var loading = true
    var ride: Ride
    var body: some View {
        List {
            Section("Summary Stats") {
                VStack {
                    HStack {
                        Text("Total Distance").bold()
                        Spacer()
                        let dist = metersToMiles(meters: ride.totalDistance)
                        Text("\(metersToMiles(meters: ride.totalDistance), specifier: "%.2f") miles")
                    }
                    Spacer()
                    HStack {
                        Text("Total Time").bold()
                        Spacer()
                        let (h,m,s) = secondsToHoursMinutesSeconds(ride.totalSeconds)
                        let formattedTime = String(format: "%02d:%02d:%02d", h, m, s)
                        Text(formattedTime)
                    }
                    Spacer()
                    HStack {
                        Text("Average Pace").bold()
                        Spacer()
                        let avgMps = ride.totalDistance / Double(ride.totalSeconds)
                        let avgMph = avgMps * 2.237
                        
                        Text("\(avgMph, specifier: "%.2f") mph")
                    }
                }.padding()
            }.headerProminence(.increased)
            if (loading) {
                ProgressView("Loading")
            } else {
                Section("Splits") {
                    ForEach(ride.splits.indices, id: \.self) {index in
                        HStack {
                            Text("Mile \(index + 1)")
                            Spacer()
                            let (splH,splM,splS) = secondsToHoursMinutesSeconds(ride.splits[index].seconds)
                            let formattedSplitTime = String(format: "%02d:%02d", splM, splS)
                            Text(formattedSplitTime)
                        }
                    }
                }.headerProminence(.increased)
                Section("Pace") {
                    if #available(iOS 16.0, *) {
                        Chart {
                            ForEach(formattedSplits) { split in
                                BarMark(
                                    x: .value("Milestone", split.milestone),
                                    y: .value("Speed", split.speed)
                                )
                                
                            }
                        }.chartXAxisLabel("Distance (miles)").chartYAxisLabel("Pace (mph)")
                            .frame(height: 250)
                    } else {
                        // Fallback on earlier versions
                        Text("IOS 16 required to display chart")
                    }
                }.headerProminence(.increased)
            }
        }.navigationTitle("Metrics").onAppear {
            for split in ride.splits {
                let speedMps = split.distance / Double(split.seconds)
                let speedMph = speedMps * 2.237
                let splitMiles = split.distance / 1609
                cumDist += Int(splitMiles)
                formattedSplits.append(FormattedSplit(milestone: cumDist, speed: Int(speedMph)))
            }
            loading = false
        }
    }
    func secondsToHoursMinutesSeconds(_ seconds: Int) -> (Int, Int, Int) {
        return (seconds / 3600, (seconds % 3600) / 60, (seconds % 3600) % 60)
    }
}
