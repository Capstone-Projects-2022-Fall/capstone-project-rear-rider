//
//  AudioAlert.swift
//  Rear Rider
//
//  Created by Bobby Palko on 10/21/22.
//

import Foundation
import AVFoundation
import UIKit

enum AlertErrors: Error {
    case fileNotFound(String)
}


/**
 * Class for managing any audio and visual alerts for the rider
 */
class RearRiderAlerts: ObservableObject {
    
    var player: AVAudioPlayer!
    var soundFile: URL! = nil
    
    @Published var frame: UIImage = UIImage()
    static var shared = RearRiderAlerts()
        
    /**
     * Takes the name of a sound file without the extension and attemts to create a player for it.
     * Audio files must be .mp3
     *  @param fileName: String - the name of the file to load
     *  @throws fileNotFound if the file was not able to be loaded
     */
    func loadSoundFile(fileName: String) throws {
        self.soundFile = Bundle.main.url(
            forResource: fileName,
            withExtension: "mp3"
        )

        if self.soundFile == nil {
            throw AlertErrors.fileNotFound("File \(fileName).mp3 not found on device!")
        }

        self.player = try! AVAudioPlayer(contentsOf: soundFile)
    }
   
    /**
     * Plays the .mp3 file if it has been loaded, else immediately returns
     */
    func playAudioAlert() {
        // do nothing if we don't have a sound file configured
        if soundFile == nil { return }
        
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
    
    func askForPic() {
        BLEManager.shared.getPicFromPi()
    }
    
    func setPic(from data: Data?) {
        guard let data = data else { return }
        frame = UIImage(data: data.advanced(by: 2)) ?? UIImage()
    }
}
