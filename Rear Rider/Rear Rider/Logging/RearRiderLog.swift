//
//  RearRiderLog.swift
//  Rear Rider
//
//  Created by Lydia Pescaru on 10/29/22.
//

import Foundation

struct Message: Identifiable {
    let id: Int
    let message: String
}

class RearRiderLog: ObservableObject {
    @Published var messages = [Message]()
    static var shared = RearRiderLog()
    
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
