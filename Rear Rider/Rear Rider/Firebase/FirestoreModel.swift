//
//  FirestoreModel.swift
//  Rear Rider
//
//  Created by Paul Sutton on 11/14/22.
//

import Foundation
import Firebase
import FirebaseFirestore
import FirebaseFirestoreSwift

@MainActor
class FirestoreModel: ObservableObject {
    
    var db = Firestore.firestore()
    var userId = Auth.auth().currentUser?.uid
    
    @Published var appError: AppError? = nil
    @Published var firestoreLoading = false
    
    struct AppError: Identifiable {
        let id = UUID().uuidString
        let errorString: String
    }
    
    enum Result {
        case success
        case failure
    }
    
    struct FirestoreResult {
        var id = UUID()
        var res: Result
        var message: String?
    }
    
    func writeRide(ride: Ride) -> FirestoreResult {
        firestoreLoading = true
        do {
            try db.collection("users").document(userId!).collection("rides").document().setData(from: ride)
            return FirestoreResult(res: .success, message: "Succesfully wrote ride to db")
        } catch {
            return FirestoreResult(res: .failure, message: error.localizedDescription)
        }
    }

}
