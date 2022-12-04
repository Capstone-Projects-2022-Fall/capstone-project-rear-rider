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
    //@EnvironmentObject var auth: AuthModel
    //@EnvironmentObject var viewRouter: ViewRouter
    @EnvironmentObject var conf: UserConfig
    @State var confAudio: String = ""
    @State var confLightPattern: Int = 1
    @State var confLightBrightness: Int = 1
    @State var confLightColor: Color = .white
    @State var confAlertToggle: Bool = true
    @State var confVehiclesOnly: Bool = true
    @State var confUnsafeDistance: Float = 17.0 // this index represents 900 in the array below
    
    var distance_text = ["50", "100", "150", "200", "250", "300",
                         "350", "400", "450", "500", "550", "600",
                         "650", "700", "750", "800", "850", "900", "950", "1000"]
    
    let audioFiles: [ConfigOptions.AudioFile] = ConfigOptions.AudioFile.allCases
    let lightPatterns: [ConfigOptions.LightPattern] = ConfigOptions.LightPattern.allCases
    let lightBrightness: [ConfigOptions.LightBrightness] = ConfigOptions.LightBrightness.allCases
    
    let alert = RearRiderAlerts.shared
    
    var body: some View {
        VStack {
            NavigationView {
                List {
                    Section {
                        Picker("Audio Alert", selection: $confAudio.onChange(setAudio), content: {
                            ForEach(audioFiles, id: \.self) {
                                audioFile in Text(audioFile.description).tag(audioFile.rawValue)
                            }
                        })
                        Toggle("Sound", isOn: $confAlertToggle.onChange(setAlert))
                        Toggle("Vehicles Only", isOn: $confVehiclesOnly.onChange(setVehiclesOnly))
                        HStack {
                            Slider(value: $confUnsafeDistance.onChange(setDistance), in: 0...19, step: 1)
                            Text("Distance: \(distance_text[Int(confUnsafeDistance)]) cm")
                        }
                    } header: {
                        Text("LiDAR")
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
//                    Button(action: {signOut()}) {
//                        Text("Sign Out").foregroundColor(.red)
//                    }

                }.navigationTitle("Options")
            }
        }
        .onAppear {
            confAudio = conf.audioFile
            confLightBrightness = conf.lightBrightness
            confLightPattern = conf.lightPattern
            confLightColor = Color.fromRGBString(rgbString: conf.lightColor)
            confAlertToggle = conf.alertToggle
            confVehiclesOnly = conf.vehiclesOnly
            confUnsafeDistance = Float(distance_text.lastIndex(of: String(conf.unsafeDistance)) ?? 0)
        }
    }
    
    // these are written out separately as to not clog up the view itself
    /**
     * Sets the config object's audio to the new selection and saves it
     */
    func setAudio(to value: String) {
        conf.audioFile = confAudio
        saveConf()
        // play audio sound
        if !conf.audioFile.isEmpty {
            try! alert.loadSoundFile(fileName: conf.audioFile)
            alert.playAudioAlert()
        }
    }
    
    /// Enable alerts
    /// - Parameter value: true to enable
    func setAlert(to value: Bool) {
        conf.alertToggle = confAlertToggle
        saveConf()
    }
    
    /// Set the unsafe distance
    /// - Parameter value: the index of distance_text array
    func setDistance(to value: Float) {
        conf.unsafeDistance = Int(distance_text[Int(confUnsafeDistance)]) ?? 0
        saveConf()
    }
    
    /// Alerts will be played only if the object detected is a vehicle
    /// - Parameter value: true or false
    func setVehiclesOnly(to value: Bool) {
        conf.vehiclesOnly = confVehiclesOnly
        saveConf()
    }
    
    /**
     * Sets the config object's light pattern to the new selection and saves it
     */
    func setLights(to value: Int) {
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
        conf.colorRGB = confLightColor.cgColor?.components
        do {
            try conf.save()
        } catch let error{
            print(error)
        }
    }
    
//    func signOut() {
//        let authResult = auth.signOutUser()
//        if (authResult.res == .success) {
//            // the warning thrown for this line is not genuine and should be ignored
//            // it is a bug with xcode 14
//            withAnimation {
//                viewRouter.currentPage = .signInPage
//            }
//        } else {
//            print("error signing out: \(authResult.message ?? "error signing out")")
//        }
//    }
}

struct OptionsView_Previews: PreviewProvider {
    static var previews: some View {
        OptionsView().environmentObject(UserConfig())
    }
}
