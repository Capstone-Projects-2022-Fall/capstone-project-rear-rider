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
    
    func signOutUser() -> AuthResult {
        do {
            try auth.signOut()
            return AuthResult(res: .success)
        } catch let signOutError as NSError {
            return AuthResult(res: .failure, message: signOutError.localizedDescription)
        }
    }
    
    func resetPassword(userEmail: String) async -> AuthResult {
        do {
            try await auth.sendPasswordReset(withEmail: userEmail)
            authLoading = false
            return AuthResult(res: .success, message: "Password reset email sent to: \(userEmail)")
        } catch {
            authLoading = false
            return AuthResult(res: .failure, message: error.localizedDescription)
        }
    }
    
}
