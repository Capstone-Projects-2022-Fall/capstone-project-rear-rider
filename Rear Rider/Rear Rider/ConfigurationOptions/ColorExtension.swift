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
    
    /**
     * Takes an rgb string "rgb(#,#,#)" and converts it to a Color
     */
    static func fromRGBString(rgbString: String) -> Color {
        let characters = CharacterSet(charactersIn: "(,)")
        let rgbValues = rgbString.components(separatedBy: characters)
        
        // default these to white if parsing fails
        var redF = 0.0
        var blueF = 0.0
        var greenF = 0.0
        
        // can we loop this somehow?
        if let red = NumberFormatter().number(from: rgbValues[1]) {
            redF = CGFloat(truncating: red)
        }
        
        if let green = NumberFormatter().number(from: rgbValues[2]) {
            greenF = CGFloat(truncating: green)
        }
        
        if let blue = NumberFormatter().number(from: rgbValues[3]) {
            blueF = CGFloat(truncating: blue)
        }
        
        return Color(UIColor(
            red: redF/255,
            green: greenF/255,
            blue: blueF/255,
            alpha: 1.0
        ))
    }
}
