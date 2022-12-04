////
////  RideHistoryView.swift
////  Rear Rider
////
////  Created by Paul Sutton on 11/9/22.
////
//
//import SwiftUI
//
//struct RideHistoryView: View {
//    var body: some View {
//        NavigationView {
//            List {
//                NavigationLink(destination: MetricsView()) {
//                    HStack {
//                        Text("11/9/2022").bold()
//                        Spacer()
//                        Text("5 miles").bold().foregroundColor(.gray)
//                    }
//                }
//                NavigationLink(destination: MetricsView()) {
//                    HStack {
//                        Text("11/9/2022").bold()
//                        Spacer()
//                        Text("5.8 miles").bold().foregroundColor(.gray)
//                    }
//                }
//                NavigationLink(destination: MetricsView()) {
//                    HStack {
//                        Text("11/10/2022").bold()
//                        Spacer()
//                        Text("6 miles").bold().foregroundColor(.gray)
//                    }
//                }
//                NavigationLink(destination: MetricsView()) {
//                    HStack {
//                        Text("11/11/2022").bold()
//                        Spacer()
//                        Text("9 miles").bold().foregroundColor(.gray)
//                    }
//                }
//                NavigationLink(destination: MetricsView()) {
//                    HStack {
//                        Text("11/12/2022").bold()
//                        Spacer()
//                        Text("3.3 miles").bold().foregroundColor(.gray)
//                    }
//                }
//            }.navigationTitle("My Rides")
//        }
//    }
//}
//
//struct RideHistoryView_Previews: PreviewProvider {
//    static var previews: some View {
//        RideHistoryView()
//    }
//}
