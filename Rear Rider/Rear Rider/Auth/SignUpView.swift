//
//  SignUpView.swift
//  timerr
//
//  Created by Robert Paul Sutton on 1/27/22.
//

import SwiftUI
import Firebase

struct SignUpView: View {
    
    @EnvironmentObject var viewRouter: ViewRouter
    @EnvironmentObject var firestoreModel: FirestoreModel
    @EnvironmentObject var auth: AuthModel
    @State var email = ""
    @State var password = ""
    @State var passwordConfirmation = ""
    @State var signUpErrorMessage = ""
    
    var body: some View {
        VStack(spacing: 15) {
            Text("Rear Rider").font(.title)
            SignUpCredentialFields(email: $email, password: $password, passwordConfirmation: $passwordConfirmation)
            Button(action: {
                signUp()
            }) {
                Text("Sign Up")
                    .bold()
                    .frame(width: 360, height: 50)
                    .background(.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                    .opacity(auth.authLoading || email.isEmpty || password.isEmpty || passwordConfirmation.isEmpty || password != passwordConfirmation ? 0.4 : 0.9)
            }
            .disabled(auth.authLoading || email.isEmpty || password.isEmpty || passwordConfirmation.isEmpty || password != passwordConfirmation ? true : false)
            if auth.authLoading {
                ProgressView()
            }
            if !signUpErrorMessage.isEmpty {
                Text("Failed creating account: \(signUpErrorMessage)")
                    .foregroundColor(.red)
            }
            Spacer()
            HStack {
                Text("Already have an account?")
                Button(action: {
                    viewRouter.currentPage = .signInPage
                }) {
                    Text("Log In")
                }
            }
            .opacity(0.9)
        }
        .padding()
    }
    
    func signUp() {
        Task {
            let authResult = await auth.signUpUser(userEmail: email, userPassword: password)
            if (authResult.res == .success) {
                withAnimation {
                    viewRouter.currentPage = .homePage
                }
            } else {
                signUpErrorMessage = authResult.message ?? "Error signing up"
            }
        }
    }
}

struct SignUpView_Previews: PreviewProvider {
    static var previews: some View {
        SignUpView()
    }
}

struct SignUpCredentialFields: View {
    
    @Binding var email: String
    @Binding var password: String
    @Binding var passwordConfirmation: String
    
    var body: some View {
        Group {
            TextField("Email", text: $email)
                .padding()
                .background(.thinMaterial)
                .cornerRadius(10)
                .textInputAutocapitalization(.never)
            SecureField("Password", text: $password)
                .padding()
                .background(.thinMaterial)
                .cornerRadius(10)
            SecureField("Confirm Password", text: $passwordConfirmation)
                .padding()
                .background(.thinMaterial)
                .cornerRadius(10)
                .border(Color.red, width: passwordConfirmation != password ? 1 : 0)
                .padding(.bottom, 30)
        }
    }
}
