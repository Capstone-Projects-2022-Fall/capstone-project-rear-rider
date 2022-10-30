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
    @EnvironmentObject var conf: UserConfig
    @State var confAudio: String = ""
    @State var confLightPattern: Int = 1
    @State var confLightBrightness: Int = 1
    @State var confLightColor: Color = .white
    
    @State var configChanged = false
    
    let audioFiles: [ConfigOptions.AudioFile] = ConfigOptions.AudioFile.allCases
    let lightPatterns: [ConfigOptions.LightPattern] = ConfigOptions.LightPattern.allCases
    let lightBrightness: [ConfigOptions.LightBrightness] = ConfigOptions.LightBrightness.allCases
    
    let alert = RearRiderAlerts()
    
    // need to wrap these in this init to get access to self for the conf variable and set these
//    init() {
//        _confAudio = State(wrappedValue: conf.audioFile)
//        _confLightPattern = State(wrappedValue: conf.lightPattern)
//        _confLightBrightness = State(wrappedValue: conf.lightBrightness)
//        _confLightColor = State(wrappedValue: Color.fromRGBString(rgbString: conf.lightColor))
//    }
    
    var body: some View {
        VStack {
            Text("Options")
            NavigationView {
                List {
                    Section {
                        Picker("Audio Alert", selection: $confAudio.onChange(setAudio), content: {
                            ForEach(audioFiles, id: \.self) {
                                audioFile in Text(audioFile.description).tag(audioFile.rawValue)
                            }
                        })
                    } header: {
                        Text("Audio")
                    }
                    Section {
                        Picker("Pattern", selection: $confLightPattern.onChange(setLights), content: {
                            ForEach(lightPatterns, id: \.self) {
                                lightPattern in Text(lightPattern.description).tag(lightPattern.rawValue)
                            }
                        })
                        Picker("Brightness", selection: $confLightBrightness.onChange(setBrightness), content: {
                            ForEach(lightBrightness, id: \.self) {
                                brightnessLevel in Text(brightnessLevel.description).tag(brightnessLevel.rawValue)
                            }
                        })
                        ColorPicker("Color", selection: $confLightColor.onChange(setColor), supportsOpacity: false
                        )
                    } header: {
                        Text("Lights")
                    }
                    Section {
                        NavigationLink(destination: RearRiderLogView()) {
                            Text("View log")
                        }
                    } header: {
                        Text("Log")
                    }
                }
            }
            .frame(maxHeight: 500)
            
            Button(action: saveConf) {
                Text("Save")
            }
            .disabled(!configChanged)
        }
        .onAppear {
            confAudio = conf.audioFile
            confLightBrightness = conf.lightBrightness
            confLightPattern = conf.lightPattern
            confLightColor = Color.fromRGBString(rgbString: conf.lightColor)
        }
    }
    
    // these are written out separately as to not clog up the view itself
    /**
     * Sets the config object's audio to the new selection and saves it
     */
    func setAudio(to value: String) {
        conf.audioFile = confAudio
        configChanged = true
        // play audio sound
        if !conf.audioFile.isEmpty {
            try! alert.loadSoundFile(fileName: conf.audioFile)
            alert.playAudioAlert()
        }
    }
    
    /**
     * Sets the config object's light pattern to the new selection and saves it
     */
    func setLights(to value: Int) {
        configChanged = true
        conf.lightPattern = confLightPattern
    }
    
    /**
     * Sets the config object's light brightness to the new selection and saves it
     */
    func setBrightness(to value: Int) {
        configChanged = true
        conf.lightBrightness = confLightBrightness
    }
    
    /**
     * Sets the config object's light color value to a string RBG representation of the new selection and saves it
     */
    func setColor(to value: Color) {
        configChanged = true
        conf.lightColor = confLightColor.toRGBString()
    }
    
    /**
     * Saves the user's configuration by calling the config's save
     */
    func saveConf() {
        conf.colorRGB = confLightColor.cgColor?.components
        do {
            try conf.save()
        } catch let error{
            print(error)
        }
        configChanged = false
    }
}

struct OptionsView_Previews: PreviewProvider {
    static var previews: some View {
        OptionsView().environmentObject(UserConfig())
    }
}
