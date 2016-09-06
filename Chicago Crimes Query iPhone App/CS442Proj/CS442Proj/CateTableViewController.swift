//
//  CateTableViewController.swift
//  CS442Proj
//
//  Created by Jiranun Jiratrakanvong, Kartikay Gautam on 6/21/16.
//  Copyright © 2016 Jiranun Jiratrakanvong, Kartikay Gautam. All rights reserved.
//

import UIKit
import CoreData

class CateTableViewController: UITableViewController {

    @IBOutlet var cateTableView: UITableView!
    var categories = ["Crime Type", "IUCR Code", "Crime Description", "Year", "Month", "Day", "Case ID"]
//    var categories = ["Day", "Month", "Year", "Time range", "Location", "IUCR Code", "Crime Type", "Crime Description"]
    var selected_cates = [(String,String)]()
    
    
    @IBAction func queryTapped() {
        var enable_case_id = false
        selected_cates = [(String,String)]()
        for row in 0...categories.count{
            let indxPath = NSIndexPath(forRow: row, inSection: 0)
            if let cell = tableView.cellForRowAtIndexPath(indxPath) as? CategoryTableViewCell{
                if cell.stateSwitch.on{
                    if let label = cell.cateLabel.text{
                        selected_cates.append((label, cell.order))
                        if label == "Case ID"{
                            enable_case_id = true
                        }
                    }
                }
            }
        }
        
        if !enable_case_id{
            selected_cates.append(("Case ID","↓"))
        }
        performSegueWithIdentifier("querySegue", sender: nil)
    }
    
    override func viewWillAppear(animated: Bool) {
        self.navigationController?.navigationBar.barStyle = UIBarStyle.Black
        self.navigationController?.navigationBar.titleTextAttributes = [NSForegroundColorAttributeName: UIColor.whiteColor()]

        self.navigationController?.setToolbarHidden(false, animated: false)
//        self.navigationController?.toolbar.barStyle = UIBarStyle.Black
//
        let exButton = UIButton(type: .Custom)
        //set image for button
        exButton.setImage(UIImage(named: "book_icon.png"), forState: .Normal)
        //add function for button
        exButton.addTarget(self, action: #selector(CateTableViewController.queryTapped), forControlEvents: .TouchUpInside)
        //set frame
        exButton.frame = CGRectMake(0, 0, 53, 31)
        
        let setting_button = UIButton(type: .Custom)
        //set image for button
        setting_button.setImage(UIImage(named: "setup_black.png"), forState: .Normal)
        //add function for button
        //        button.addTarget(self, action: "fbButtonPressed", forControlEvents: UIControlEvents.TouchUpInside)
        //set frame
        setting_button.frame = CGRectMake(0, 0, 53, 31)
        
        let fileEx = UIBarButtonItem(customView: exButton)
        let settingBut = UIBarButtonItem(customView: setting_button)
        let space = UIBarButtonItem(barButtonSystemItem: .FlexibleSpace, target: nil, action: nil)
        settingBut.customView = setting_button
        self.setToolbarItems([fileEx,space,settingBut], animated: false)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Uncomment the following line to preserve selection between presentations
        // self.clearsSelectionOnViewWillAppear = false
        self.navigationItem.title = "Categories"
        
        
        
        // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
        let queryButton = UIBarButtonItem(barButtonSystemItem: UIBarButtonSystemItem.Search, target: self, action: #selector(CateTableViewController.queryTapped))
        queryButton.tintColor = UIColor.whiteColor()
        self.navigationItem.rightBarButtonItem = queryButton
        self.setEditing(true, animated: false)
        cateTableView.setEditing(true, animated: false)
        
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
        return categories.count
    }

    
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier("CateCell", forIndexPath: indexPath) as! CategoryTableViewCell
        let cate_name = categories[indexPath.row]
        cell.cateLabel?.text = cate_name
//        cell.stateSwitch.setOn(true, animated: true)
        // Configure the cell...
        return cell
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
//            tableView.deleteRowsAtIndexPaths([indexPath], withRowAnimation: .Fade)
            
        } else if editingStyle == .Insert {
            // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
        }    
    }
    */
    
    override func tableView(tableView: UITableView, editingStyleForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCellEditingStyle {
        return UITableViewCellEditingStyle.None
    }
    
    
    // Override to support rearranging the table view.
    override func tableView(tableView: UITableView, moveRowAtIndexPath fromIndexPath: NSIndexPath, toIndexPath: NSIndexPath) {
        let itemToMove = categories[fromIndexPath.row]
        categories.removeAtIndex(fromIndexPath.row)
        categories.insert(itemToMove, atIndex: toIndexPath.row)
    }
 

    
    // Override to support conditional rearranging of the table view.
    override func tableView(tableView: UITableView, canMoveRowAtIndexPath indexPath: NSIndexPath) -> Bool {
        // Return false if you do not want the item to be re-orderable.
        return true
    }
 

    
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.identifier == "querySegue" {
            let dest = segue.destinationViewController as! QueryTableViewController
            QueryTableViewController.currentCategory = 0
            QueryTableViewController.sCategories = self.selected_cates
            dest.currentCateStr = QueryTableViewController.sCategories[QueryTableViewController.currentCategory].0
            dest.navigationItem.title = dest.currentCateStr
            dest.conditions = QueryTableViewController.sQueryManager.getConditions(dest.currentCateStr,order:QueryTableViewController.sCategories[QueryTableViewController.currentCategory].1)
            
        }
    }
    

}
