//
//  ViewRouter.swift
//  Rear Rider
//
//  Created by Paul Sutton on 11/14/22.
//

import SwiftUI

class ViewRouter: ObservableObject {
    @Published var currentPage: Page = .signInPage
}

enum Page {
    case signUpPage
    case signInPage
    case forgotPasswordPage
    case homePage
}
