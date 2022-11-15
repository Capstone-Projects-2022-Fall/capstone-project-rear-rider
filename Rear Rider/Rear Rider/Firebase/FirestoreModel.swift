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

class FirestoreModel: ObservableObject {
    
    var db = Firestore.firestore()
    
    struct AppError: Identifiable {
        let id = UUID().uuidString
        let errorString: String
    }
    
    @Published var appError: AppError? = nil
    
}
