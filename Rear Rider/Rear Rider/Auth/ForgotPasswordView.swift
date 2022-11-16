//
//  ForgotPasswordView.swift
//  timerr
//
//  Created by Paul Sutton on 5/31/22.
//

import SwiftUI
import Firebase

struct ForgotPasswordView: View {
    @EnvironmentObject var auth: AuthModel
    @EnvironmentObject var viewRouter: ViewRouter
    @State var email = ""
    
    struct AppError: Identifiable {
        let id = UUID().uuidString
        let errorString: String
        let titleString: String
    }
    
    @State var appError: AppError? = nil
    
    var body: some View {
        VStack(spacing: 15) {
            Text("Reset password")
            EmailCredential(email: $email)
            Button(action: {
                reset()}) {
                Text("Reset Password")
                    .bold()
                    .frame(width: 360, height: 50)
                    .background(.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                    .opacity(auth.authLoading || email.isEmpty ? 0.4 : 0.9)
            }
                .disabled(auth.authLoading || email.isEmpty)
            
            if (auth.authLoading) {
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
    
    func reset() {
        Task {
            let authResult = await auth.resetPassword(userEmail: email)
            if (authResult.res == .success) {
                appError = AppError(errorString: "Sent reset password to \(email)", titleString: "Password Reset")
            } else {
                appError = AppError(errorString: authResult.message ?? "error reseting password", titleString: "Error")
            }
        }
    }
    
    
    struct ForgotPasswordView_Previews: PreviewProvider {
        static var previews: some View {
            SignUpView()
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
