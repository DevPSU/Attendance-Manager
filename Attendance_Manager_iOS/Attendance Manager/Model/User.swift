//
//  User.swift
//  Attendance Manager
//
//  Created by Nick Fink on 3/2/19.
//  Copyright © 2019 PSU Attendance Management Team. All rights reserved.
//

import Foundation

struct User
{
    var email : String!
    var bearer_token : String!
    var name : String!
}

struct UserService {
    static func logInUser (withEmail userEmail : String, withPassword userPassword : String, done: @escaping ((_ error: String?) -> Void)) {
        let headers = [
            "Content-Type": "application/json",
            "cache-control": "no-cache"
        ]
        let parameters = [
            "email": userEmail,
            "password": userPassword,
            "should_expire": ""
            ] as [String : Any]
        
        
        let postData = try! JSONSerialization.data(withJSONObject: parameters, options: [])
        let request = NSMutableURLRequest(url: NSURL(string: "http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/auth/login")! as URL,
                                          cachePolicy: .useProtocolCachePolicy,
                                          timeoutInterval: 10.0)
        request.httpMethod = "POST"
        request.allHTTPHeaderFields = headers
        request.httpBody = postData as Data
        
        let session = URLSession.shared
        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
            if (error != nil) {
                print(error)
            } else {
                let httpResponse = response as? HTTPURLResponse
                do {
                    let json = try JSONSerialization.jsonObject(with: data!, options: [])
                    let dictionary = json as! [String: Any]
                    if let errorMessage = dictionary["error"] as? String
                    {
                        print(errorMessage)
                        return
                    }
                    print (dictionary["bearer_token"] as? String)
                    
                } catch {
                    print ("JSONSerialization error:", error)
                    
                }
                print(httpResponse?.statusCode)
            }
        })
        
        dataTask.resume()
    }
}
