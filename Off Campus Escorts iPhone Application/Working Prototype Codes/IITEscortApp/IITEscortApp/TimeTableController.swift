//
//  TimeTableController.swift
//  IITEscortApp
//
//  Created by Jiranun Jiratrakanvong on 7/26/16.
//  Copyright © 2016 Jiranun Jiratrakanvong. All rights reserved.
//

import UIKit

class TimeTableController: UITableViewController {
    var timetable = [String]()
    var user_type = "Passenger"
    var user_name = ""
    var time_selected = ""
    let queryManager = QueryManager()
    let nPassenger = 4
    
    func logout()
    {
        self.navigationController?.popToRootViewControllerAnimated(true)
    }
    
    override func viewWillAppear(animated: Bool) {
        self.navigationController?.navigationBarHidden = false
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.navigationItem.title = "Round Trips"
        let appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
        timetable = appDelegate.time
        // Uncomment the following line to preserve selection between presentations
        // self.clearsSelectionOnViewWillAppear = false

        // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
        // self.navigationItem.rightBarButtonItem = self.editButtonItem()
        let logoutButton = UIBarButtonItem(title: "Logout", style: .Plain, target: self, action: #selector(self.logout))
        self.navigationItem.leftBarButtonItem = logoutButton
        if user_name == "driver"{
            user_type = "Driver"
            let clearAllButton = UIBarButtonItem(title: "Clear All", style: .Plain, target: self, action: #selector(self.clearAll))
            self.navigationItem.rightBarButtonItem = clearAllButton

        }
        self.refreshControl?.addTarget(self, action: #selector(self.refresh), forControlEvents: UIControlEvents.ValueChanged)
    }
    
    func clearAll(){
        if self.queryManager.clearAll(){
            print("Data cleared")
            tableView.reloadData()
        }
    }

    func refresh(sender:AnyObject)
    {
        // Updating your data here...
        
        self.tableView.reloadData()
        self.refreshControl?.endRefreshing()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    // MARK: - Table view data source

    override func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        // #warning Incomplete implementation, return the number of sections
        return 1
    }

    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of rows
        return timetable.count
    }

    
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier("TimeCell", forIndexPath: indexPath) as! TimeCell
        cell.timeLabel?.text = timetable[indexPath.row]
        let students = queryManager.getStudents(timetable[indexPath.row])
        let remain = nPassenger - students.count
        var available:String = ""
        
        if user_type == "Passenger"{
            if remain > 0{
                for _ in 0...remain-1{
                    available.append("✅" as Character)
                }
            }
            if students.count > 0{
                for _ in 0...students.count-1{
                    available.append("❌" as Character)
                }
            }
        }
        else{
            if students.count > 0{
                for _ in 0...students.count-1{
                    available.append("👤" as Character)
                }
            }
        }
        cell.available?.text = available
        //        cell.stateSwitch.setOn(true, animated: true)
        // Configure the cell...
        return cell
    }
    
    override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        self.time_selected = self.timetable[indexPath.row]
        if user_type == "Passenger"{
            let passengers = queryManager.getStudents(timetable[indexPath.row])
            if nPassenger-passengers.count > 0{
                performSegueWithIdentifier("PickupSegue", sender: nil)
            }else{
                let alert = UIAlertController(title: "No Available Seat", message: "Please select another round trip", preferredStyle: UIAlertControllerStyle.Alert)
                alert.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.Default, handler: nil))
                self.presentViewController(alert, animated: true, completion: nil)
            }
        }else{
            performSegueWithIdentifier("DriverSegue", sender: nil)
        }
        tableView.deselectRowAtIndexPath(indexPath, animated: true)
        
    }

    /*
    // Override to support conditional editing of the table view.
    override func tableView(tableView: UITableView, canEditRowAtIndexPath indexPath: NSIndexPath) -> Bool {
        // Return false if you do not want the specified item to be editable.
        return true
    }
    */

    /*
    // Override to support editing the table view.
    override func tableView(tableView: UITableView, commitEditingStyle editingStyle: UITableViewCellEditingStyle, forRowAtIndexPath indexPath: NSIndexPath) {
        if editingStyle == .Delete {
            // Delete the row from the data source
            tableView.deleteRowsAtIndexPaths([indexPath], withRowAnimation: .Fade)
        } else if editingStyle == .Insert {
            // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
        }    
    }
    */

    /*
    // Override to support rearranging the table view.
    override func tableView(tableView: UITableView, moveRowAtIndexPath fromIndexPath: NSIndexPath, toIndexPath: NSIndexPath) {

    }
    */

    /*
    // Override to support conditional rearranging of the table view.
    override func tableView(tableView: UITableView, canMoveRowAtIndexPath indexPath: NSIndexPath) -> Bool {
        // Return false if you do not want the item to be re-orderable.
        return true
    }
    */

    
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.identifier == "PickupSegue" {
            let dest = segue.destinationViewController as! PickupViewController
            dest.selected_time = self.time_selected
            dest.user_name = self.user_name
        }
        else if segue.identifier == "DriverSegue" {
            let dest = segue.destinationViewController as! DriverViewController
            dest.selected_time = self.time_selected
        }
    }
 

}
