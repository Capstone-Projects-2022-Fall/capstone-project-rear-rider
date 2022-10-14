//
//  RecordingExtension.swift
//  Rear Rider
//
//  Created by Bobby Palko on 10/14/22.
//

import SwiftUI
import ReplayKit

extension View {
    
    func startRecording(completion: @escaping (Error?)->()) {
        let recorder = RPScreenRecorder.shared()
        recorder.startRecording(handler: completion)
    }
    
    func stopRecording()async throws->URL {
        let name = UUID().uuidString + ".mov"
        let url = FileManager.default.temporaryDirectory.appendingPathComponent(name)
        
        let recorder = RPScreenRecorder.shared()
        try await recorder.stopRecording(withOutput: url)
        
        return url
    }
    
    // Custom modifier to share video
    func shareSheet(show: Binding<Bool>, items: [Any?])->some View {
        return self
            .sheet(isPresented: show) {} content: {
                let items = items.compactMap { item -> Any? in
                    return item
                }
                
                if !items.isEmpty {
                    ShareSheet(items: items)
                }
            }
    }
}
