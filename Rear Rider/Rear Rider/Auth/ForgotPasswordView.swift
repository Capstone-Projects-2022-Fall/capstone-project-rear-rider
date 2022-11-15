//
//  ForgotPasswordView.swift
//  timerr
//
//  Created by Paul Sutton on 5/31/22.
//

import SwiftUI
import Firebase

struct ForgotPasswordView: View {
    
    @EnvironmentObject var viewRouter: ViewRouter
    @State var email = ""
    @State var processing = false
    
    struct AppError: Identifiable {
        let id = UUID().uuidString
        let errorString: String
        let titleString: String
    }
    
    @State var appError: AppError? = nil
    
    var body: some View {
        VStack(spacing: 15) {
            Logo()
            Spacer()
            EmailCredential(email: $email)
            Button(action: {
                resetPassword(userEmail: email)}) {
                Text("Reset Password")
                    .bold()
                    .frame(width: 360, height: 50)
                    .background(.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                    .opacity(processing || email.isEmpty ? 0.4 : 0.9)
            }
            .disabled(processing || email.isEmpty)
            
            if processing {
                ProgressView()
            }
            Spacer()
            HStack {
                Button(action: {
                    viewRouter.currentPage = .signInPage
                }) {
                    Text("Back to Log In")
                }
            }
            .opacity(0.9)
        }.alert(item: $appError) { appAlert in
            Alert(title: Text("Message"),
                  message: Text(appAlert.errorString)
            )
        }.padding()
    }
    
    func resetPassword(userEmail: String) {
        processing = true
        Auth.auth().sendPasswordReset(withEmail: userEmail) { (error) in
                if error == nil {
                    processing = false
                    appError = AppError(errorString: "Your password has been reset. An email with instructions was sent to \(userEmail)", titleString: "Success")
                } else  {
                    processing = false
                    appError = AppError(errorString: "Could not reset password for \(userEmail)", titleString: "Error")
                }
        }
    }
    
    
    struct ForgotPasswordView_Previews: PreviewProvider {
        static var previews: some View {
            SignUpView()
        }
    }
    
    struct Logo: View {
        @Environment(\.colorScheme) var colorScheme
        var body: some View {
            Image(colorScheme == .light ? "LightLogo" : "DarkLogo")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(width: 300, height: 150)
                .padding(.top, 70)
        }
    }
    
    struct EmailCredential: View {
        
        @Binding var email: String
        
        var body: some View {
            TextField("Email", text: $email)
                .padding()
                .background(.thinMaterial)
                .cornerRadius(10)
                .textInputAutocapitalization(.never)
            
        }
    }
}
