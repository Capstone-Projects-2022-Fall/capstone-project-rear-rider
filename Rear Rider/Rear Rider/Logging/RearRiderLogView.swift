//
//  RearRiderLogView.swift
//  Rear Rider
//
//  Created by Lydia Pescaru on 10/29/22.
//

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
