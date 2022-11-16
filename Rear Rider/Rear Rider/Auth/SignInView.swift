//
//  SignInView.swift
//  timerr
//
//  Created by Robert Paul Sutton on 1/27/22.
//

import SwiftUI
import Firebase

struct SignInView: View {
    @EnvironmentObject var auth: AuthModel
    @EnvironmentObject var viewRouter: ViewRouter
    @State var email = ""
    @State var password = ""
    @State var signInErrorMessage = ""
    
    var body: some View {
        VStack(spacing: 15) {
            Text("Rear Rider").font(.title)
            SignInCredentialFields(email: $email, password: $password)
            HStack {
                Spacer()
                Button(action: {
                    viewRouter.currentPage = .forgotPasswordPage
                }) {
                    Spacer()
                    Text("Forgot Password?")
                }
            }
            Button(action: {
                signIn()
            }) {
                Text("Log In")
                    .bold()
                    .frame(width: 360, height: 50)
                    .background(.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                    .opacity(!auth.authLoading && !email.isEmpty && !password.isEmpty ? 0.9 : 0.4)
            }
            .disabled(!auth.authLoading && !email.isEmpty && !password.isEmpty ? false : true)
            
            if auth.authLoading {
                ProgressView()
            }
            if !signInErrorMessage.isEmpty {
                Text("Error logging in: \(signInErrorMessage)")
                    .foregroundColor(.red)
            }
            Spacer()
            HStack {
                Text("Don't have an account?")
                Button(action: {
                    viewRouter.currentPage = .signUpPage
                }) {
                    Text("Sign Up")
                }
            }
            .opacity(0.9)
        }.padding().onAppear {
            //user is logged in
            if Auth.auth().currentUser?.uid != nil {
                viewRouter.currentPage = .homePage
            }
        }
    }
    
    func signIn() {
        Task {
            let authResult = await auth.signInUser(userEmail: email, userPassword: password)
            if (authResult.res == .success) {
                withAnimation {
                    viewRouter.currentPage = .homePage
                }
            } else {
                signInErrorMessage = authResult.message ?? "Error signing in"
            }
        }
    }
    
}

struct SignInView_Previews: PreviewProvider {
    static var previews: some View {
        SignInView()
    }
}

struct SignInCredentialFields: View {
    
    @Binding var email: String
    @Binding var password: String
    
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
        }
    }
}
