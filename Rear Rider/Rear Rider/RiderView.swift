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
    @ObservedObject var alert = RearRiderAlerts.shared
    
    var body: some View {
        VStack {
            Image(uiImage: alert.frame)
            
            // temporary
            Button {
                alert.askForPic()
            } label: {
                Text("Get")
            }
        }
    }
}

struct RiderView_Previews: PreviewProvider {
    static var previews: some View {
        RiderView().environmentObject(BLEManager())
    }
}
