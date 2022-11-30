//
//  ViewController.swift
//  Rear Rider
//
//  Created by Paul Sutton on 11/14/22.
//

import SwiftUI

struct ViewController: View {
    
    @EnvironmentObject var viewRouter: ViewRouter
    
    var body: some View {
        switch viewRouter.currentPage {
        case .signUpPage:
            SignUpView()
        case .signInPage:
            SignInView()
        case .forgotPasswordPage:
            ForgotPasswordView()
        case .homePage:
            HomeView()
        }
    }
}

struct ViewController_Previews: PreviewProvider {
    static var previews: some View {
        ViewController().environmentObject(ViewRouter())
    }
}

