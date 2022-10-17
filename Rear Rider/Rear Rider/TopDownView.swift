//
//  TopDownView.swift
//  Rear Rider
//
//  Created by Paul Sutton on 10/17/22.
//

import SwiftUI

struct TopDownView: View {
    var body: some View {
        VStack {
            HStack {
                AlertComponent(message: "Car")
                Spacer()
                Image("biker").resizable()
                    .frame(width: 150, height: 350)
                Spacer()
                AlertComponent(message: "Bike")
            }
            AlertComponent(message: "Car")
        }.padding()
    }
}

struct TopDownView_Previews: PreviewProvider {
    static var previews: some View {
        TopDownView()
    }
}
