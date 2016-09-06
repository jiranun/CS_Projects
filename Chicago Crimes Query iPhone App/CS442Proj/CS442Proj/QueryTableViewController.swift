//
//  QueryTableViewController.swift
//  CS442Proj
//
//  Created by Jiranun Jiratrakanvong, Kartikay Gautam on 6/21/16.
//  Copyright © 2016 Jiranun Jiratrakanvong, Kartikay Gautam. All rights reserved.
//

import UIKit

class QueryTableViewController: UITableViewController {
    static var sCategories = [(String,String)]()
    static var sQueryManager = QueryManager()
    static var currentCategory = 0
    
    @IBOutlet weak var settingsTabbar: UITabBarItem!
    
    var conditions = [String]()
    var currentCateStr = ""
    
    override func viewDidLoad() {
        super.viewDidLoad()
    
        // Uncomment the following line to preserve selection between presentations
        // self.clearsSelectionOnViewWillAppear = false

        // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
        // self.navigationItem.rightBarButtonItem = self.editButtonItem()
       
    }
    
    func gotoRoot()
    {
        QueryTableViewController.sQueryManager.removeCondition()
        self.navigationController?.popToRootViewControllerAnimated(true)
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
//        exButton.addTarget(self, action: #selector(CateTableViewController.queryTapped), forControlEvents: .TouchUpInside)
        //set frame
        exButton.frame = CGRectMake(0, 0, 53, 31)
        
        let setting_button = UIButton(type: .Custom)
        //set image for button
        setting_button.setImage(UIImage(named: "setup_black.png"), forState: .Normal)
        //add function for button
        setting_button.addTarget(self, action: #selector(self.gotoRoot), forControlEvents: .TouchUpInside)
        //set frame
        setting_button.frame = CGRectMake(0, 0, 53, 31)
        
        let fileEx = UIBarButtonItem(customView: exButton)
        let settingBut = UIBarButtonItem(customView: setting_button)
        let space = UIBarButtonItem(barButtonSystemItem: .FlexibleSpace, target: nil, action: nil)
        settingBut.customView = setting_button
        self.setToolbarItems([fileEx,space,settingBut], animated: false)
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
        return self.conditions.count
    }

    
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
//        let cell = tableView.dequeueReusableCellWithIdentifier("reuseIdentifier", forIndexPath: indexPath)
        let cell = UITableViewCell()
        // Configure the cell...
        cell.textLabel?.text = self.conditions[indexPath.row]
        cell.accessoryType = .DisclosureIndicator
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
    func addCondition(selected_row:Int){
        QueryTableViewController.sQueryManager.addCondition(self.currentCateStr, condition: conditions[selected_row])
    }
    
    override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        addCondition(indexPath.row)
        
        if self.navigationItem.title == "Case ID"{
            performSegueWithIdentifier("showDetail", sender: nil)
        }
        else{
            QueryTableViewController.currentCategory += 1
            performSegueWithIdentifier("addCondition", sender: nil)
        }
    }
    
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.identifier == "addCondition"{
            let dest = segue.destinationViewController as! QueryTableViewController
            dest.currentCateStr = QueryTableViewController.sCategories[QueryTableViewController.currentCategory].0
            dest.navigationItem.title = dest.currentCateStr
            dest.conditions = QueryTableViewController.sQueryManager.getConditions(dest.currentCateStr, order:QueryTableViewController.sCategories[QueryTableViewController.currentCategory].1)
        }
        if segue.identifier == "showDetail"{
            let dest = segue.destinationViewController as! DetailViewController
            if let result_case = QueryTableViewController.sQueryManager.getCase(){
                dest.result_case = result_case
                dest.navigationItem.title = result_case.id
            }
            
        }
    }
    
    override func willMoveToParentViewController(parent: UIViewController?) {
        super.willMoveToParentViewController(parent)
        if parent == nil {
            QueryTableViewController.sQueryManager.removeCondition(self.currentCateStr)
            QueryTableViewController.currentCategory -= 1
        }
    }
}
