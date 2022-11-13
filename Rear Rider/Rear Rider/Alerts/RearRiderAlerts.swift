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
    var mLModel = ImageIdentification()
    var player: AVAudioPlayer!
    var soundFile: URL! = nil
    
    @Published var frame: UIImage = UIImage()
    static var shared = RearRiderAlerts()
    
    var picData = NSMutableData()
    var pic_size:Int = 0
    var pic_first_time:Bool = true
    
    
    /// When this is set, the transfer of the packets will commence
    var pic_packets:Int = 0 {
        didSet {
            RearRiderLog.shared.addLog(from: "Alerts", message: "Pic size: \(pic_size); Packets: \(pic_packets)")
            BLEManager.shared.getPicPacket(index: 0)
        }
    }
    
    /// This is set every time a new packet arrives; then a new packet will be requested
    var packet_recv: UInt8 = 0 {
        didSet {
            if packet_recv == pic_packets {
                frame = UIImage(data: picData as Data) ?? UIImage()
                mLModel.detectObjects(image: frame)
                pic_first_time = true
                picData = NSMutableData()
                if mLModel.detected_objs.isEmpty { askForPic() } // if no objects detect ask for another pic
            }
            else {
                BLEManager.shared.getPicPacket(index: packet_recv)
            }
        }
    }
        
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
    
    /// Asks the RPi for the picture's metadata (size and number of packets)
    func askForPic() {
        mLModel.detected_objs.removeAll()
        mLModel.clearBndRects()
        BLEManager.shared.getPicInfo()
    }
}
