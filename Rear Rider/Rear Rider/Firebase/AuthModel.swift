//
//  AuthModel.swift
//  Rear Rider
//
//  Created by Paul Sutton on 11/14/22.
//

import Foundation
import Firebase

@MainActor
class AuthModel: ObservableObject {

    var auth = Auth.auth()
    var db = FirestoreModel().db
    @Published var authLoading = false
    
    enum Result {
        case success
        case failure
    }
    
    struct AuthResult {
        var id = UUID()
        var res: Result
        var message: String?
    }
    
    func signOutUser() -> AuthResult {
        let firebaseAuth = Auth.auth()
        do {
            try firebaseAuth.signOut()
            return AuthResult(res: .success)
        } catch let signOutError as NSError {
            print("Error signing out: %@", signOutError)
            return AuthResult(res: .failure, message: signOutError.localizedDescription)
        }
    }
    
    func signUpUser(userEmail: String, userPassword: String) async -> AuthResult {
        authLoading = true
        do {
            let authResult = try await auth.createUser(withEmail: userEmail, password: userPassword)
            try await self.db.collection("users").document(authResult.user.uid).setData([
                "email": userEmail,
                "uid": authResult.user.uid
            ])
            authLoading = false
            return AuthResult(res: .success, message: "Successfully created user")
        } catch {
            authLoading = false
            return AuthResult(res: .failure, message: error.localizedDescription)
        }
    }
    
    func signInUser(userEmail: String, userPassword: String) async -> AuthResult {
        authLoading = true
        do {
            try await auth.signIn(withEmail: userEmail, password: userPassword)
            authLoading = false
            return AuthResult(res: .success, message: "Success signing in")
        } catch {
            authLoading = false
            return AuthResult(res: .failure, message: error.localizedDescription)
        }
    }
    
}
