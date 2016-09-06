//
//  DriverViewController.swift
//  IITEscortApp
//
//  Created by Jiranun Jiratrakanvong on 7/29/16.
//  Copyright © 2016 Jiranun Jiratrakanvong. All rights reserved.
//

import UIKit
import MapKit

class DriverViewController: UIViewController, MKMapViewDelegate {
    var selected_time = ""
    let queryManager = QueryManager()
    var dropoff_locations = [String:(Double,Double)]()
    var pickup_locations = [String:(Double,Double)]()
    
    @IBOutlet weak var myMap: MKMapView!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        self.navigationItem.title = selected_time
        let passengers = queryManager.getStudents(selected_time)
        
        let appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
        dropoff_locations = appDelegate.dropoff_locations
        pickup_locations = appDelegate.pickup_locations
        var annotations = [MKAnnotation]()
        var loc_pas = [String:[String]]()
        
        for p in passengers{
            if let from = p.from{
                if loc_pas[from] != nil{
                    loc_pas[from]?.append(p.name!)
                }
                else{
                    loc_pas[from] = [p.name!]
                }
            }
            
            if let to = p.to{
                if loc_pas[to] != nil{
                    loc_pas[to]?.append(p.name!)
                }
                else{
                    loc_pas[to] = [p.name!]
                }
            }
        }
        
        for lp in loc_pas{
            let place = lp.0
            let pgs = lp.1
            var coords = (0.0,0.0)
            
            if pickup_locations.keys.contains(place){
                coords = pickup_locations[place]!
            }
            else if dropoff_locations.keys.contains(place){
                coords = dropoff_locations[place]!
            }
            
            let coord = CLLocationCoordinate2DMake(Double(coords.0), Double(coords.1))
            let dropPin = MKPointAnnotation()
            dropPin.coordinate = coord
            dropPin.title = place
            let sub = pgs.joinWithSeparator(",")
            dropPin.subtitle = sub
            annotations.append(dropPin)
        }
        
        myMap.addAnnotations(annotations)
        
        let coord = CLLocationCoordinate2DMake(41.834674, -87.626599)
        let latDelta: CLLocationDegrees = 0.05
        let lonDelta: CLLocationDegrees = 0.05
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
            if pickup_locations.keys.contains(annotation.title!!){
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
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
