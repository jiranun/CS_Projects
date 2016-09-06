//
//  ViewController.swift
//  IITEscortApp
//
//  Created by Jiranun Jiratrakanvong on 7/26/16.
//  Copyright © 2016 Jiranun Jiratrakanvong. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var username: UITextField!
    @IBOutlet weak var password: UITextField!
    @IBOutlet weak var LoginButton: UIButton!
    let queryManager = QueryManager()
    var passenger = [String]()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    override func viewWillAppear(animated: Bool) {
        self.navigationController?.navigationBarHidden = true
        username.text = ""
        password.text = ""
        username.resignFirstResponder()
        password.resignFirstResponder()
    }
    
    @IBAction func screen_Tapped(sender: UITapGestureRecognizer) {
        username.resignFirstResponder()
        password.resignFirstResponder()
    }
    @IBAction func LoginTapped(sender: UIButton) {
        if let uname = username.text{
            if uname == ""{
                print("please enter username!")
            }
            else{
                if let p = queryManager.getReservedSeat(uname){
                    self.passenger = p
                    performSegueWithIdentifier("AlreadyReserved", sender: nil)
                }else{
                    performSegueWithIdentifier("StudentReserve", sender: nil)
                }
                
            }
        }
        else{
            print("please enter username!")
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if segue.identifier == "StudentReserve" {
            let DestViewController = segue.destinationViewController as! TimeTableController
            DestViewController.user_name = username.text!
        }
        if segue.identifier == "AlreadyReserved" {
            let DestViewController = segue.destinationViewController as! ReservedSeatViewController
            DestViewController.passenger = self.passenger
        }
    }
}

