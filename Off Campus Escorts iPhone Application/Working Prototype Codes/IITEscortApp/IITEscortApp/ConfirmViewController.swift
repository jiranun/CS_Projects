//
//  ConfirmViewController.swift
//  IITEscortApp
//
//  Created by Jiranun Jiratrakanvong on 7/26/16.
//  Copyright © 2016 Jiranun Jiratrakanvong. All rights reserved.
//

import UIKit
import MapKit

class ConfirmViewController: UIViewController , MKMapViewDelegate{

    @IBOutlet weak var username: UILabel!
    @IBOutlet weak var myMap: MKMapView!
    @IBOutlet weak var time: UILabel!
    @IBOutlet weak var pickup: UILabel!
    @IBOutlet weak var dropoff: UILabel!
    var user_info = [String]() 
    let queryManager = QueryManager()
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        username.text = user_info[0]
        time.text = user_info[1]
        pickup.text = user_info[2]
        dropoff.text = user_info[3]
        self.navigationItem.title = "Confirmation"
        let appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
        let dropoff_locations = appDelegate.dropoff_locations
        let pickup_locations = appDelegate.pickup_locations
        var annotations = [MKAnnotation]()
        var center_lad = 0.0
        var center_long = 0.0
        if let from = pickup.text{
            if let pickup_coord = pickup_locations[from]{
                let coord = CLLocationCoordinate2DMake(Double(pickup_coord.0), Double(pickup_coord.1))
                let dropPin = MKPointAnnotation()
                dropPin.coordinate = coord
                dropPin.title = "From"
                dropPin.subtitle = from
                center_lad += pickup_coord.0
                center_long += pickup_coord.1
                annotations.append(dropPin)
            }
        }
        
        if let to = dropoff.text{
            if let dropoff_coord = dropoff_locations[to]{
                let coord = CLLocationCoordinate2DMake(Double(dropoff_coord.0), Double(dropoff_coord.1))
                let dropPin = MKPointAnnotation()
                dropPin.coordinate = coord
                dropPin.title = "To"
                dropPin.subtitle = to
                center_lad += dropoff_coord.0
                center_long += dropoff_coord.1
                annotations.append(dropPin)
            }
        }
        myMap.addAnnotations(annotations)
        
        let coord = CLLocationCoordinate2DMake(center_lad/2.0, center_long/2.0)
        let latDelta: CLLocationDegrees = 0.015
        let lonDelta: CLLocationDegrees = 0.015
        let span:MKCoordinateSpan = MKCoordinateSpanMake(latDelta, lonDelta)
        let region = MKCoordinateRegionMake(coord, span)
        myMap.setRegion(region, animated: true)
    }
    
    func mapView(mapView: MKMapView, viewForAnnotation annotation: MKAnnotation) -> MKAnnotationView? {
        if annotation is MKUserLocation {
            return nil
        }
    
        let reuseId = "pin"
        var pinView = mapView.dequeueReusableAnnotationViewWithIdentifier(reuseId) as? MKPinAnnotationView
        if pinView == nil {
            pinView = MKPinAnnotationView(annotation: annotation, reuseIdentifier: reuseId)
            if annotation.subtitle! == user_info[2]{
                pinView?.pinTintColor = UIColor.blackColor()
            }
            pinView!.canShowCallout = true
        }
        else {
            pinView?.annotation = annotation
        }
        
        return pinView
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func confirmTapped(sender: UIButton) {
        queryManager.addStudent(user_info[0], time: user_info[1], from: user_info[2], to: user_info[3])
        performSegueWithIdentifier("confirmed", sender: nil)
    }

    @IBAction func cancelTapped(sender: UIButton) {
        performSegueWithIdentifier("BackToTime", sender: nil)
    }
    
    
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.identifier == "BackToTime"{
            let dest = segue.destinationViewController as! TimeTableController
            dest.user_name = self.user_info[0]
        }
        if segue.identifier == "confirmed"{
            let dest = segue.destinationViewController as! ReservedSeatViewController
            dest.passenger = self.user_info
        }
    }
 

}
