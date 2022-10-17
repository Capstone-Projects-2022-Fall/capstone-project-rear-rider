//
//  AlertComponent.swift
//  Rear Rider
//
//  Created by Paul Sutton on 10/17/22.
//

import SwiftUI

struct AlertComponent: View {
    var message: String
    var body: some View {
        Text(message).foregroundColor(.white).bold().font(.title).padding().background(.red).cornerRadius(10).shadow(radius: 15)
        
    }
}

struct AlertComponent_Previews: PreviewProvider {
    static var previews: some View {
        AlertComponent(message: "Car")
    }
}
