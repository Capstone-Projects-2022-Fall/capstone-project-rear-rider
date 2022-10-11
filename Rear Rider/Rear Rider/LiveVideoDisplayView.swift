//
//  LiveVideoDisplayView.swift
//  Rear Rider
//
//  Created by Paul Sutton on 10/11/22.
//

import SwiftUI

struct LiveVideoDisplayView: View {
    @StateObject private var model = FrameHandler()
    var body: some View {
        FrameView(image: model.frame)
                    .ignoresSafeArea()
    }
}

struct LiveVideoDisplayView_Previews: PreviewProvider {
    static var previews: some View {
        LiveVideoDisplayView()
    }
}
