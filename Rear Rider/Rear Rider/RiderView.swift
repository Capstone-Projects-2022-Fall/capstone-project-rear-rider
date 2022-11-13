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
            ZStack {
                ForEach (RearRiderAlerts.shared.mLModel.bndRectsCopy) { rect in
                    Rectangle()
                        .frame(width: rect.rect.width, height: rect.rect.height)
                        .border(.yellow, width: 1)
                        .zIndex(20)
                        .foregroundColor(.clear)
                        .position(x: rect.rect.minX + rect.rect.width / 2, y: rect.rect.minY - rect.rect.height / 2)
                }
                
                Image(uiImage: alert.frame)
                    .resizable()
                    .scaledToFit()
            }
            .scaledToFit()
            
            // temporary
            HStack {
                Button {
                    alert.askForPic()
                } label: {
                    Text("Get")
                }
            }
        }
    }
}

struct RiderView_Previews: PreviewProvider {
    static var previews: some View {
        RiderView().environmentObject(BLEManager())
    }
}
