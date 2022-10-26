//
//  ColorExtension.swift
//  Rear Rider
//
//  Created by Bobby Palko on 10/26/22.
//

import Foundation
import SwiftUI
import UIKit

/**
 * Extends the SwiftUI Color struct to separate the RGBA values for easier manipulation on the Rear Rider device
 */
extension Color {
    var components: (red: CGFloat, green: CGFloat, blue: CGFloat, opacity: CGFloat) {
        typealias NativeColor = UIColor

        var r: CGFloat = 0
        var g: CGFloat = 0
        var b: CGFloat = 0
        var o: CGFloat = 0

        guard NativeColor(self).getRed(&r, green: &g, blue: &b, alpha: &o) else {
            // default to white on fail
            return (0, 0, 0, 0)
        }

        return (r, g, b, o)
    }
    
    /**
     * Takes the RGB values and returns a string such as "rbg(#,#,#)"
     */
    func toRGBString() -> String {
        let red:Int = Int(round(self.components.red * 255))
        let green:Int = Int(round(self.components.green * 255))
        let blue:Int = Int(round(self.components.blue * 255))
        
        return "rgb(\(red),\(green),\(blue))"
    }
}
