// RearRider
//
// Calin Pescaru
//
// October 2022
//
// Bluetooth Manager
//
// A simple logger for the RearRider app.

import Foundation

struct Message: Identifiable {
    let id: Int
    let message: String
}

/// A logger for the RearRider app
/// The format is "date~time # from - message" where from is the class where the action is happening
class RearRiderLog: ObservableObject {
    @Published var messages = [Message]()
    static var shared = RearRiderLog()
    
    /// Add a new log
    /// - Parameters:
    ///   - source: The class where the action is happening
    ///   - msg: The desired message to be logged
    func addLog(from source: String, message msg: String) {
        var log = ""
        let date = Date()
        let calendar = NSCalendar.current
        let requestedComponents: Set<Calendar.Component> = [
            .year,
            .month,
            .day,
            .hour,
            .minute,
            .second
        ]
        
        let currentDate = calendar.dateComponents(requestedComponents, from: date)
        
        log += String(currentDate.month!) + "/" + String(currentDate.day!) +
        "/" + String(currentDate.year!) + "~" + String(currentDate.hour!) + ":" +
        String(currentDate.minute!) + ":" + String(currentDate.second!) + " # "
        log += source + " - " + msg + "\n"
        
        let message = Message(id: messages.count, message: log)
        messages.append(message)
    }
}
