// RearRider
//
// Calin Pescaru
//
// October 2022
//
// Bluetooth UI
//
// Simple SwiftUI to test the BLEManager functionality.

import SwiftUI

struct BluetoothView: View {
    @EnvironmentObject var bleManager: BLEManager
    @State private var msg = ""
    @State private var showDisconnectAlert = false
    @State private var selection = ""
    
    var body: some View {
        VStack(spacing: 10) {
            Text("Bluetooth Device")
                .font(.largeTitle)
                .frame(maxWidth: .infinity, alignment: .center)
            
            List(bleManager.statusMsgs) { statusMsg in
                HStack {
                    Text(statusMsg.msg)
                }
            }
            .frame(height: 300)
            
            Spacer()
            
            Text("STATUS")
                .font(.headline)
            if bleManager.isSwitchedOn {
                Text("Bluetooth is switched on")
                    .foregroundColor(.green)
            }
            else {
                Text("Bluetooth is NOT switched on")
                    .foregroundColor(.red)
            }
            
            Spacer()
            
            List(bleManager.messages) { message in
                HStack {
                    Text(message.msg)
                }
            }
            .frame(height: 200)
            
            HStack {
                VStack(spacing: 10) {
                    Button(action: {
                        bleManager.startScanning()
                    }) {
                        Text("Connect to Pi")
                    }
                    
                    Button(action: {
                        showDisconnectAlert = true
                    }) {
                        Text("Disconnect")
                    }
                }
                .padding()
                .alert("Are you sure?", isPresented: $showDisconnectAlert) {
                    Button ("Yes") {
                        bleManager.disconnectBLE()
                    }
                    Button ("No", role: .cancel) {}
                }
                
                Spacer()
                
                VStack(spacing: 10) {
                    TextField("Send message", text: $msg)
                    Button(action: {
                        bleManager.sendMsg(message: msg)
                        msg = ""
                    }) {
                        Text("Send")
                    }
                }
                .padding()
            }
            
            Spacer()
        }
    }
}

struct BluetoothView_Previews: PreviewProvider {
    static var previews: some View {
        BluetoothView()
    }
}
