//
//  DetailViewController.swift
//  CS442Proj
//
//  Created by Jiranun Jiratrakanvong, Kartikay Gautam on 6/27/16.
//  Copyright © 2016 Jiranun Jiratrakanvong, Kartikay Gautam. All rights reserved.
//

import UIKit
import MapKit

class DetailViewController: UIViewController {
    var queryManager = QueryManager()
    var result_case:Case?
    
    @IBOutlet weak var case_date: UILabel!
    @IBOutlet weak var crime_number: UILabel!
    @IBOutlet weak var crime_type: UILabel!
    @IBOutlet weak var crime_des: UILabel!
    @IBOutlet weak var mapView: MKMapView!
    
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

    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        if result_case != nil{
            if let fulldate = result_case?.fulldate{
                case_date.text = fulldate.description
            }
            if let crime = result_case?.toCrime{
                if let crime_num = crime.crime_number{
                    crime_number.text = crime_num
                }
                if let crime_t = crime.type{
                    crime_type.text = crime_t
                    crime_des.lineBreakMode = .ByWordWrapping
                }
                if let crime_d = crime.crime_description{
                    crime_des.text = crime_d
                    crime_des.lineBreakMode = .ByWordWrapping
                }
            }
            
            if let lat = result_case?.latitude{
                if let long = result_case?.longitude{
                    let coord = CLLocationCoordinate2DMake(Double(lat), Double(long))
                    let dropPin = MKPointAnnotation()
                    
                    dropPin.coordinate = coord
                    dropPin.title = self.navigationItem.title
                    mapView.addAnnotation(dropPin)
                    
                    let latDelta: CLLocationDegrees = 0.05
                    let lonDelta: CLLocationDegrees = 0.05
                    let span:MKCoordinateSpan = MKCoordinateSpanMake(latDelta, lonDelta)
                    let region = MKCoordinateRegionMake(coord, span)
                    mapView.setRegion(region, animated: true)
                }
            }
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
