//
//  ActiveView.swift
//  Rear Rider
//
//  Created by Paul Sutton on 11/30/22.
//

import SwiftUI

struct ActiveView: View {
    @StateObject var trackingManager = TrackingManager()
    var body: some View {
        NavigationView {
            switch trackingManager.authorizationStatus {
            case .notDetermined:
                AnyView(RequestLocationView())
                    .environmentObject(trackingManager)
            case .restricted:
                ErrorView(errorText: "Location use is restricted. Please enable location use while app is in use in settings")
            case .denied:
                ErrorView(errorText: "The app does not have location permissions. Please enable them in settings.")
            case .authorizedAlways, .authorizedWhenInUse:
                TrackingView().environmentObject(trackingManager)
            default:
                Text("Unexpected status")
            }
        }
    }
}

struct RequestLocationView: View {
    @EnvironmentObject var trackingManager: TrackingManager
    
    var body: some View {
        VStack {
            Image(systemName: "location.circle")
                .resizable()
                .frame(width: 100, height: 100, alignment: .center)
                .foregroundColor(/*@START_MENU_TOKEN@*/.blue/*@END_MENU_TOKEN@*/)
            Button(action: {
                trackingManager.requestPermission()
            }, label: {
                Label("Allow tracking", systemImage: "location")
            })
            .padding(10)
            .foregroundColor(.white)
            .background(Color.blue)
            .clipShape(RoundedRectangle(cornerRadius: 8))
            Text("We need your permission to track you.")
                .foregroundColor(.gray)
                .font(.caption)
        }
    }
}

struct ErrorView: View {
    var errorText: String
    
    var body: some View {
        VStack {
            Image(systemName: "xmark.octagon")
                .resizable()
                .frame(width: 100, height: 100, alignment: .center)
            Text(errorText)
        }
        .padding()
        .foregroundColor(.white)
        .background(Color.red)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

struct ActiveView_Previews: PreviewProvider {
    static var previews: some View {
        ActiveView()
    }
}
