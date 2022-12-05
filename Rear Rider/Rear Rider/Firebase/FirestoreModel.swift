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
    private var userId = Auth.auth().currentUser?.uid
    
    @Published var appError: AppError? = nil
    @Published var firestoreLoading = false
    @Published var rides = [Ride]()
    
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
        var content: Any?
    }
    
    func writeRide(ride: Ride) -> FirestoreResult {
        firestoreLoading = true
        do {
            try db.collection("users").document(userId!).collection("rides").document().setData(from: ride)
            firestoreLoading = false
            return FirestoreResult(res: .success, message: "Succesfully wrote ride to db")
        } catch {
            firestoreLoading = false
            return FirestoreResult(res: .failure, message: error.localizedDescription)
        }
    }
    
    func getRides() {
        if (rides.isEmpty) {
            firestoreLoading = true
        }
        db.collection("users").document(userId!).collection("rides").order(by: "createdTime", descending: true).addSnapshotListener() { (querySnapshot, err) in
            if let err = err {
                self.firestoreLoading = false
                print("Error getting documents: \(err)")
            } else {
                self.rides.removeAll()
                for document in querySnapshot!.documents {
                    do {
                        let docData = try document.data(as: Ride.self)
                        self.rides.append(docData)
                    } catch {
                        print(error)
                        self.firestoreLoading = false
                    }
                }
            }
            self.firestoreLoading = false
        }
    }

}
