// RearRider
//
// Calin Pescaru
//
// October 2022
//
// Bluetooth Manager
//
// The view associate with the RearRider logger.

import SwiftUI

struct RearRiderLogView: View {
    @EnvironmentObject var log: RearRiderLog
    
    var body: some View {
        VStack {
            ScrollView {
                ForEach(log.messages, id: \.id) { element in
                    Text(element.message)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .font(.system(size: 10))
                }
            }
        }
    }
}

struct RearRiderLogView_Previews: PreviewProvider {
    static var previews: some View {
        RearRiderLogView().environmentObject(RearRiderLog())
    }
}
