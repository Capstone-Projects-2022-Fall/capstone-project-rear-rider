//
//  RideHistoryView.swift
//  Rear Rider
//
//  Created by Paul Sutton on 11/9/22.
//

import SwiftUI

struct RideHistoryView: View {
    @EnvironmentObject var firestoreModel: FirestoreModel
    var body: some View {
        NavigationView {
            List {
                if (firestoreModel.firestoreLoading) {
                    ProgressView()
                } else {
                    ForEach(firestoreModel.rides.indices, id: \.self) {index in
                        NavigationLink(destination: MetricsView(ride: firestoreModel.rides[index])) {
                            HStack {
                                Text(Formatter.shared.timestampToString(timestamp: firestoreModel.rides[index].createdTime)).bold()
                                Spacer()
                                Text("\(metersToMiles(meters: firestoreModel.rides[index].totalDistance), specifier: "%.2f") miles").bold().foregroundColor(.gray)
                            }
                        }
                    }
                }
            }.navigationTitle("My Rides").onAppear {
                firestoreModel.getRides()
            }
        }
    }
}

struct RideHistoryView_Previews: PreviewProvider {
    static var previews: some View {
        RideHistoryView()
    }
}
