////
////  MetricsView.swift
////  Rear Rider
////
////  Created by Paul Sutton on 11/9/22.
////
//
//import SwiftUI
//import Charts
//
//struct MetricsView: View {
//    var body: some View {
//        List {
//            Section("Summary Stats") {
//                VStack {
//                    HStack {
//                        Text("Total Distance").bold()
//                        Spacer()
//                        Text("5.8 miles")
//                    }
//                    Spacer()
//                    HStack {
//                        Text("Total Time").bold()
//                        Spacer()
//                        Text("23 minutes")
//                    }
//                    Spacer()
//                    HStack {
//                        Text("Average Pace").bold()
//                        Spacer()
//                        Text("12.4 mph")
//                    }
//                }.padding()
//            }.headerProminence(.increased)
//            Section("Splits") {
//                HStack {
//                    Text("Mile 1")
//                    Spacer()
//                    Text("4 min 03 sec")
//                }
//                HStack {
//                    Text("Mile 2")
//                    Spacer()
//                    Text("4 min 20 sec")
//                }
//                HStack {
//                    Text("Mile 3")
//                    Spacer()
//                    Text("3 min 49 sec")
//                }
//                HStack {
//                    Text("Mile 4")
//                    Spacer()
//                    Text("4 min 15 sec")
//                }
//                HStack {
//                    Text("Mile 5")
//                    Spacer()
//                    Text("4 min 10 sec")
//                }
//            }.headerProminence(.increased)
//            Section("Pace") {
//                if #available(iOS 16.0, *) {
//                    Chart {
//                        LineMark(
//                            x: .value("Distance", "1 mi"),
//                            y: .value("Value", 16)
//                        )
//                        LineMark(
//                            x: .value("Distance", "2 mi"),
//                            y: .value("Value", 14)
//                        )
//                        LineMark(
//                            x: .value("Distance", "3 mi"),
//                            y: .value("Value", 17.5)
//                        )
//                        LineMark(
//                            x: .value("Distance", "4 mi"),
//                            y: .value("Value", 15)
//                        )
//
//                        LineMark(
//                            x: .value("Distance", "5 mi"),
//                            y: .value("Value", 15.3)
//                        )
//
//                    }.chartXAxisLabel("Distance (mi)").chartYAxisLabel("Pace (mph)")
//                    .frame(height: 250)
//                } else {
//                    // Fallback on earlier versions
//                    Text("IOS 16 required to display chart")
//                }
//            }.headerProminence(.increased)
//        }.navigationTitle("Metrics")
//    }
//}
//
//struct MetricsView_Previews: PreviewProvider {
//    static var previews: some View {
//        MetricsView()
//    }
//}
