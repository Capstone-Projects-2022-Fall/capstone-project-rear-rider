//
//  Dates.swift
//  timerr
//
//  Created by Paul Sutton on 5/9/22.
//

import Foundation
import FirebaseFirestore
// date formatter singleton
class Formatter {
    static let shared = Formatter(dateFormatter: DateFormatter())
    let dateFormatter: DateFormatter
    private init(dateFormatter: DateFormatter) {
        self.dateFormatter = dateFormatter
        dateFormatter.dateFormat = "MM/dd/yy h:mm a"
    }
    func timestampToString(timestamp: Timestamp?) -> String {
        if ((timestamp) != nil) {
        let unformattedDate = timestamp!.dateValue()
        let formattedDateString = dateFormatter.string(from: unformattedDate)
        return formattedDateString
        } else {
            return ""
        }
    }
}
