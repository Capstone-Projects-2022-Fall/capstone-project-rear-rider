//
//  RecordingView.swift
//  Rear Rider
//
//  Created by Bobby Palko on 10/14/22.
//

import SwiftUI

struct RecordingView: View {
    
    @State var isRecording: Bool = false
    @State var url: URL?
    @State var shareVideo: Bool = false
    
    var body: some View {
        Spacer()
            .overlay(alignment: .center) {
                Button {
                    if isRecording {
                        // Task for async
                        Task {
                            do {
                                self.url = try await stopRecording()
                                isRecording = false
                                shareVideo.toggle()
                            } catch {
                                print(error.localizedDescription)
                            }
                        }
                        
                    } else {
                        startRecording { error in
                            if let error = error {
                                print(error.localizedDescription)
                                return
                            }
                            isRecording = true
                        }
                    }
                } label: {
                    // recording icon
                    Image(systemName: isRecording ? "record.circle.fill" : "record.circle")
                        .font(.largeTitle)
                        .foregroundColor(isRecording ? .red : .white)
                }
            }
            .shareSheet(show: $shareVideo, items: [url])
    }
}

struct RecordingView_Previews: PreviewProvider {
    static var previews: some View {
        RecordingView()
    }
}
