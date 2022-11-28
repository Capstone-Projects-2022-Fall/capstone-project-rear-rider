//
//  MetricsModel.swift
//  Rear Rider
//
//  Created by Paul Sutton on 11/15/22.
//

import Foundation
import FirebaseFirestore
import FirebaseFirestoreSwift

struct Split: Hashable, Codable, Identifiable {
    var id = UUID()
    var seconds: Int
    var distance: Int
}

struct Ride: Hashable, Codable, Identifiable {
    @DocumentID var id: String?
    @ServerTimestamp var createdTime: Timestamp?
    var totalDistance: Int
    var metric: String
    var creatorId: String
}