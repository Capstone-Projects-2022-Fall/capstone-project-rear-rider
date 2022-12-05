//
//  TrackingView.sÏwift
//  Rear Rider
//
//  Created by Paul Sutton on 11/30/22.
//

import SwiftUI

struct TrackingView: View {
    @EnvironmentObject var trackingManager: TrackingManager
    @EnvironmentObject var db: FirestoreModel
    @State private var loading = false
    @State private var err = false
    var body: some View {
        VStack {
            HStack{
                VStack(alignment: .leading){
                    Text("Elapsed Time").bold().foregroundColor(.gray)
                    let formattedTime = String(format: "%02d:%02d:%02d", trackingManager.hours, trackingManager.minutes, trackingManager.seconds)
                    Text(formattedTime).font(.system(size: 50)).fontWeight(.bold).monospacedDigit().padding(.bottom, 20)
                    Text("Distance").bold().foregroundColor(.gray)
                    Text("\(metersToMiles(meters: trackingManager.cummulativeDistance), specifier: "%.2f") miles").font(.system(size: 50)).fontWeight(.bold).monospacedDigit().padding(.bottom, 20)
                    Text("Speed").bold().foregroundColor(.gray)
                    if (trackingManager.mode == .started) {
                        let mph = (trackingManager.lastSeenLocation?.speed ?? 0) * 2.237
                        Text("\(String(format: "%.2f", mph)) mph").font(.system(size: 50)).fontWeight(.bold).monospacedDigit().padding(.bottom, 20)
                    } else {
                        Text("-/-").font(.system(size: 50)).fontWeight(.bold).padding(.bottom, 20)
                    }
                    if (loading) {
                        ProgressView("Writing ride to db")
                    }
                }
                Spacer()
            }.padding(25)
            
            Spacer()
            VStack{
            if trackingManager.mode == .stopped {
                Button(action: {
                    self.trackingManager.start()
                }) {
                    Text("Start")
                        .bold()
                        .frame(width: 275, height: 50)
                        .background(.green)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
            }
                if trackingManager.mode == .started {
                    Button(action: {
                        self.trackingManager.pause()
                    }) {
                        Text("Pause")
                            .bold()
                            .frame(width: 150, height: 50)
                            .background(.red)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                }
                if trackingManager.mode == .paused {
                    HStack {
                        Spacer()
                        Button(action: {
                            self.trackingManager.start()
                        }) {
                            Text("Resume")
                                .bold()
                                .frame(width: 150, height: 50)
                                .background(.green)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                        Spacer()
                        Button(action: {
                            createRun()
                            
                        }) {
                            Text("End Ride")
                                .bold()
                                .frame(width: 150, height: 50)
                                .background(.red)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                        Spacer()
                    }
                }
            }.padding(.bottom, 40)
        }.frame(maxHeight: .infinity, alignment: .bottom).alert("Error writing ride to DB", isPresented: $err) {
            Button("OK", role: .cancel) { }
        }
    }
    
    func createRun() {
        loading = true
        let result = db.writeRide(ride: Ride(totalDistance: trackingManager.cummulativeDistance, totalSeconds: trackingManager.secondsElapsed, metric: "meters", creatorId: db.userId!, splits: trackingManager.splits))
        if (result.res == .success) {
            self.trackingManager.stop()
            loading = false
        }
        if (result.res == .failure) {
            self.trackingManager.stop()
            loading = false
            err = true
        }
    }
}



func metersToMiles(meters: Double) -> Double {
    return meters/1609
}


struct TrackingView_Previews: PreviewProvider {
    static var previews: some View {
        TrackingView()
    }
}
