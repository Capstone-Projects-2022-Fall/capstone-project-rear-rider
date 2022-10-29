// RearRider
//
// Calin Pescaru
//
// October 2022
//
// Main UI for RearRider

import SwiftUI

struct RiderView: View {
    @EnvironmentObject var bleManager: BLEManager
    
    var body: some View {
        VStack {
            Text("Rear Rider")
        }
//        .onAppear() {
//            if bleManager.connected {
//                bleManager.toggleNotifyCharacteristic(enabled: true)
//            }
//        }
    }
}

struct RiderView_Previews: PreviewProvider {
    static var previews: some View {
        RiderView().environmentObject(BLEManager())
    }
}
