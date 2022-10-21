//
//  AudioAlert.swift
//  Rear Rider
//
//  Created by Bobby Palko on 10/21/22.
//

import Foundation
import AVFoundation

enum AlertErrors: Error {
    case fileNotFound(String)
}

struct RearRiderAlerts {
    
    var player: AVAudioPlayer!
    var soundFile: URL!
    
    init(fileName: String) throws {
        soundFile = Bundle.main.url(
            forResource: fileName,
            withExtension: "mp3"
        )

        if soundFile == nil {
            throw AlertErrors.fileNotFound("File \(fileName).mp3 not found on device!")
        }

        player = try! AVAudioPlayer(contentsOf: soundFile)  
    }
    
   
    
    func playAudioAlert() {
        do {
            try AVAudioSession.sharedInstance().setCategory(
                AVAudioSession.Category.playback,
                options: AVAudioSession.CategoryOptions.duckOthers
            )

            try AVAudioSession.sharedInstance().setActive(true)
            player.play()
        } catch let error {
            print(error)
        }
    }
}
