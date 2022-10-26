//
//  OptionsView.swift
//  Rear Rider
//
//  Created by Bobby Palko on 10/25/22.
//

import SwiftUI

// This binding extension lets us attach our change handler directly to the binding instead of the view, letting us place the observer next to the thing its observing instead of having onChange() modifiers everywhere.
extension Binding {
    func onChange(_ handler: @escaping (Value) -> Void) -> Binding<Value> {
        Binding(
            get: { self.wrappedValue },
            set: { newValue in
                self.wrappedValue = newValue
                handler(newValue)
            }
        )
    }
}

struct OptionsView: View {
    @ObservedObject var conf = UserConfig()
    @State var confAudio: String = ""
    @State var confLightPattern: String = ""
    @State var confLightBrightness: Int = 1
    @State var confLightColor: Color = .white
    
    let audioFiles: [ConfigOptions.AudioFile] = ConfigOptions.AudioFile.allCases
    let lightPatterns: [ConfigOptions.LightPattern] = ConfigOptions.LightPattern.allCases
    let lightBrightness: [ConfigOptions.LightBrightness] = ConfigOptions.LightBrightness.allCases
    
    // need to wrap these in this init to get access to the conf variable and set these
    init() {
        self._confAudio = State(wrappedValue: conf.audioFile)
        self._confLightPattern = State(wrappedValue: conf.lightPattern)
        self._confLightBrightness = State(wrappedValue: conf.lightBrightness)
//        self._confLightColor = State
    }
    
    var body: some View {
        VStack {
            Text("Options")
            List {
                Picker("Audio Alert", selection: $confAudio.onChange(setAudio), content: {
                    ForEach(audioFiles, id: \.self) {
                        audioFile in Text(audioFile.description).tag(audioFile.rawValue)
                    }
                })
                Picker("Light Pattern", selection: $confLightPattern.onChange(setLights), content: {
                    ForEach(lightPatterns, id: \.self) {
                        lightPattern in Text(lightPattern.description).tag(lightPattern.rawValue)
                    }
                })
                Picker("Light Pattern", selection: $confLightBrightness.onChange(setBrightness), content: {
                    ForEach(lightBrightness, id: \.self) {
                        brightnessLevel in Text(brightnessLevel.description).tag(brightnessLevel.rawValue)
                    }
                })
                ColorPicker("Color", selection: $confLightColor.onChange(setColor), supportsOpacity: false
                )
                Text("Color Value: \(confLightColor.toRGBString())")

            }
        }
    }
    
    /**
     * Sets the config object's audio to the new selection and saves it
     */
    func setAudio(to value: String) {
        conf.audioFile = confAudio
        saveConf()
    }
    
    /**
     * Sets the config object's light pattern to the new selection and saves it
     */
    func setLights(to value: String) {
        conf.lightPattern = confLightPattern
        saveConf()
    }
    
    /**
     * Sets the config object's light brightness to the new selection and saves it
     */
    func setBrightness(to value: Int) {
        conf.lightBrightness = confLightBrightness
        saveConf()
    }
    
    /**
     * Sets the config object's light color value to a string RBG representation of the new selection and saves it
     */
    func setColor(to value: Color) {
        conf.lightColor = confLightColor.toRGBString()
        saveConf()
    }
    
    /**
     * Saves the user's configuration by calling the config's save
     */
    func saveConf() {
        do {
            try conf.save()
        } catch let error{
            print(error)
        }
    }
}

struct OptionsView_Previews: PreviewProvider {
    static var previews: some View {
        OptionsView()
    }
}
