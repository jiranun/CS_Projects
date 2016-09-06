//
//  DropoffViewController.swift
//  IITEscortApp
//
//  Created by Jiranun Jiratrakanvong on 7/26/16.
//  Copyright © 2016 Jiranun Jiratrakanvong. All rights reserved.
//

import UIKit
import MapKit

class DropoffViewController: UIViewController, MKMapViewDelegate {

    @IBOutlet weak var dropoffMap: MKMapView!
    var user_name = ""
    var selected_time = ""
    var pickup_location = ""
    var dropoff_location = ""
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.navigationItem.title = "Select a Drop-off Location"
        let appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
        let dropoff_locations = appDelegate.dropoff_locations
        var annotations = [MKAnnotation]()
        for p in dropoff_locations{
            let coord = CLLocationCoordinate2DMake(Double(p.1.0), Double(p.1.1))
            let dropPin = MKPointAnnotation()
            dropPin.coordinate = coord
            dropPin.title = p.0
            annotations.append(dropPin)
        }
        dropoffMap.addAnnotations(annotations)
        
        let coord = CLLocationCoordinate2DMake(41.834674, -87.626599)
        let latDelta: CLLocationDegrees = 0.04
        let lonDelta: CLLocationDegrees = 0.04
        let span:MKCoordinateSpan = MKCoordinateSpanMake(latDelta, lonDelta)
        let region = MKCoordinateRegionMake(coord, span)
        dropoffMap.setRegion(region, animated: true)
        
    }
    
    func mapView(mapView: MKMapView, viewForAnnotation annotation: MKAnnotation) -> MKAnnotationView? {
        
        if annotation is MKUserLocation {
            //return nil so map view draws "blue dot" for standard user location
            return nil
        }
        
        let reuseId = "pin"
        
        var pinView = mapView.dequeueReusableAnnotationViewWithIdentifier(reuseId) as? MKPinAnnotationView
        if pinView == nil {
            pinView = MKPinAnnotationView(annotation: annotation, reuseIdentifier: reuseId)
            pinView!.canShowCallout = true
            pinView!.animatesDrop = true
            
            let button = UIButton(type: .Custom)
            button.setImage(UIImage(named: "images/select.png"), forState: .Normal)
            button.frame = CGRectMake(0, 0, 50, 25)
            pinView!.rightCalloutAccessoryView = button
        }
        else {
            pinView!.annotation = annotation
        }
        return pinView
    }
    
    func mapView(mapView: MKMapView, annotationView view: MKAnnotationView, calloutAccessoryControlTapped control: UIControl) {
        if let ann = view.annotation{
            if let loc = ann.title{
                if let  loc_st = loc{
                    dropoff_location = loc_st
                    performSegueWithIdentifier("ConfirmSegue", sender: nil)
                }
            }
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    
    // MARK: - Navigation
    
    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.identifier == "ConfirmSegue"{
            let dest = segue.destinationViewController as! ConfirmViewController
            dest.user_info.append(self.user_name)
            dest.user_info.append(self.selected_time)
            dest.user_info.append(self.pickup_location)
            dest.user_info.append(self.dropoff_location)
        }
    }

}
