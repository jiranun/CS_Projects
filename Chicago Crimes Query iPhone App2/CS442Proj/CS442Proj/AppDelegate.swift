// This application has been implemented by
//
// 1. Jiranun Jiratrakanvong A20337992
// 2. Kartikay Gautam A20360708
// In order to generate CoreData from SQLITE, self.sqLiteToCD() in AppDelegate.swift needs to be called. It is called only when you build the app for the first time. All subsequent bypasses to the function have been automated , no need for commenting out.

//
//  AppDelegate.swift
//  CS442Proj
//
//  Created by Jiranun Jiratrakanvong, Kartikay Gautam on 6/20/16.
//  Copyright © 2016 Jiranun Jiratrakanvong, Kartikay Gautam. All rights reserved.
//

import UIKit
import CoreData


@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?
    var fetchResult = [Case]()
    
    var dictionary_plist: NSMutableDictionary?
    var status: Bool?

    func application(application: UIApplication, didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?) -> Bool {
        // Override point for customization after application launch.

        readPlistToCheckStatusOfCoreDB()
        
        status = dictionary_plist?.valueForKey("core_db_status") as? Bool
        
        if !(status!){
            
            self.sqLiteToCD()
            
            dictionary_plist?.setValue(true, forKey: "core_db_status")
            
            updateCoreDbStatusInPlist()
        }
        
        self.checkCD()
        
        return true
    }
    
    func checkCD() {
        let fetchRequest = NSFetchRequest(entityName: "Case")
        fetchRequest.sortDescriptors = [NSSortDescriptor(key: "id", ascending: true)]
        do {
            self.fetchResult = try managedObjectContext.executeFetchRequest(fetchRequest) as! [Case]
            print("\(fetchResult.count) cases have been fetched.")
        } catch {
            abort()
        }
    }
    
    func readPlistToCheckStatusOfCoreDB(){
        
        let paths = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true) as NSArray
        let documentsDirectory = paths[0]
        let path = documentsDirectory.stringByAppendingPathComponent("init.plist")
        
        let fileManager = NSFileManager.defaultManager()
        
        if (!(fileManager.fileExistsAtPath(path)))
        {
            let bundle : NSString = NSBundle.mainBundle().pathForResource("init", ofType: "plist")!
            
            do {
                try fileManager.copyItemAtPath(bundle as String, toPath: path)
            } catch let error as NSError {
                print("Unable to copy file. ERROR: \(error.localizedDescription)")
            }
        }
        
        if let dictionary = NSMutableDictionary(contentsOfFile: path){
            dictionary_plist = dictionary
        }
    }
    
    func updateCoreDbStatusInPlist(){
        
        let paths = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true) as NSArray
        let documentsDirectory = paths[0]
        let path = documentsDirectory.stringByAppendingPathComponent("init.plist")
        dictionary_plist!.writeToFile(path, atomically: true)
    }

    func applicationWillResignActive(application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(application: UIApplication) {
        // Called as part of the transition from the background to the inactive state; here you can undo many of the changes made on entering the background.
    }

    func applicationDidBecomeActive(application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
        // Saves changes in the application's managed object context before the application terminates.
        self.saveContext()
    }

    // MARK: - Core Data stack

    lazy var applicationDocumentsDirectory: NSURL = {
        // The directory the application uses to store the Core Data store file. This code uses a directory named "cs442.CS442Proj" in the application's documents Application Support directory.
        let urls = NSFileManager.defaultManager().URLsForDirectory(.DocumentDirectory, inDomains: .UserDomainMask)
        return urls[urls.count-1]
    }()

    lazy var managedObjectModel: NSManagedObjectModel = {
        // The managed object model for the application. This property is not optional. It is a fatal error for the application not to be able to find and load its model.
        let modelURL = NSBundle.mainBundle().URLForResource("CS442Proj", withExtension: "momd")!
        return NSManagedObjectModel(contentsOfURL: modelURL)!
    }()

    lazy var persistentStoreCoordinator: NSPersistentStoreCoordinator = {
        // The persistent store coordinator for the application. This implementation creates and returns a coordinator, having added the store for the application to it. This property is optional since there are legitimate error conditions that could cause the creation of the store to fail.
        // Create the coordinator and store
        let coordinator = NSPersistentStoreCoordinator(managedObjectModel: self.managedObjectModel)
        let url = self.applicationDocumentsDirectory.URLByAppendingPathComponent("SingleViewCoreData.sqlite")
        var failureReason = "There was an error creating or loading the application's saved data."
        do {
            try coordinator.addPersistentStoreWithType(NSSQLiteStoreType, configuration: nil, URL: url, options: nil)
        } catch {
            // Report any error we got.
            var dict = [String: AnyObject]()
            dict[NSLocalizedDescriptionKey] = "Failed to initialize the application's saved data"
            dict[NSLocalizedFailureReasonErrorKey] = failureReason

            dict[NSUnderlyingErrorKey] = error as NSError
            let wrappedError = NSError(domain: "YOUR_ERROR_DOMAIN", code: 9999, userInfo: dict)
            // Replace this with code to handle the error appropriately.
            // abort() causes the application to generate a crash log and terminate. You should not use this function in a shipping application, although it may be useful during development.
            NSLog("Unresolved error \(wrappedError), \(wrappedError.userInfo)")
            abort()
        }
        
        return coordinator
    }()

    lazy var managedObjectContext: NSManagedObjectContext = {
        // Returns the managed object context for the application (which is already bound to the persistent store coordinator for the application.) This property is optional since there are legitimate error conditions that could cause the creation of the context to fail.
        let coordinator = self.persistentStoreCoordinator
        var managedObjectContext = NSManagedObjectContext(concurrencyType: .MainQueueConcurrencyType)
        managedObjectContext.persistentStoreCoordinator = coordinator
        return managedObjectContext
    }()

    // MARK: - Core Data Saving support

    func saveContext () {
        if managedObjectContext.hasChanges {
            do {
                try managedObjectContext.save()
            } catch {
                // Replace this implementation with code to handle the error appropriately.
                // abort() causes the application to generate a crash log and terminate. You should not use this function in a shipping application, although it may be useful during development.
                let nserror = error as NSError
                NSLog("Unresolved error \(nserror), \(nserror.userInfo)")
                abort()
            }
        }
    }
    
    func initCrimeCaseEntity(db: COpaquePointer!) {
        let queryStatementString = "SELECT DISTINCT IUCR,\"Primary Type\",Description FROM Crimes_2015;"
        var queryStatement: COpaquePointer = nil
        if sqlite3_prepare_v2(db, queryStatementString, -1, &queryStatement, nil) == SQLITE_OK {
            while sqlite3_step(queryStatement) == SQLITE_ROW {
                
                let queryResultCol1 = sqlite3_column_text(queryStatement, 0)
                let queryResultCol2 = sqlite3_column_text(queryStatement, 1)
                let queryResultCol3 = sqlite3_column_text(queryStatement, 2)
                let IUCR = String.fromCString(UnsafePointer<CChar>(queryResultCol1))!
                let PrimaryType = String.fromCString(UnsafePointer<CChar>(queryResultCol2))!
                let Description = String.fromCString(UnsafePointer<CChar>(queryResultCol3))!
                
                let crime_entity = NSEntityDescription.entityForName("Crime", inManagedObjectContext: managedObjectContext)
                let case_entity = NSEntityDescription.entityForName("Case", inManagedObjectContext: managedObjectContext)
                
                let crime = NSManagedObject(entity: crime_entity!, insertIntoManagedObjectContext: managedObjectContext) as! Crime
                crime.crime_number = IUCR
                crime.type = PrimaryType
                crime.crime_description = Description
                let case_set = NSMutableSet()
            
                var queryStatement2: COpaquePointer = nil
                let queryCases = "SELECT \"Case Number\",Date,Latitude,Longitude FROM Crimes_2015 WHERE IUCR=\""+IUCR+"\";"
                if sqlite3_prepare_v2(db, queryCases, -1, &queryStatement2, nil) == SQLITE_OK {
                    while sqlite3_step(queryStatement2) == SQLITE_ROW {
                        let queryCaseCol1 = sqlite3_column_text(queryStatement2, 0)
                        let queryCaseCol2 = sqlite3_column_text(queryStatement2, 1)
                        let queryCaseCol3 = sqlite3_column_text(queryStatement2, 2)
                        let queryCaseCol4 = sqlite3_column_text(queryStatement2, 3)
                        let case_number = String.fromCString(UnsafePointer<CChar>(queryCaseCol1))!
                        let datestr = String.fromCString(UnsafePointer<CChar>(queryCaseCol2))!
                        let latitude = String.fromCString(UnsafePointer<CChar>(queryCaseCol3))!
                        let longitude = String.fromCString(UnsafePointer<CChar>(queryCaseCol4))!
                        
                        let a_case = NSManagedObject(entity: case_entity!, insertIntoManagedObjectContext: managedObjectContext) as! Case
                        a_case.id = case_number
                        
                        let dateFormatter = NSDateFormatter()
                        dateFormatter.dateFormat = "MM-dd-yyyy hh:mm:ss a"
                        if let date = dateFormatter.dateFromString(datestr){
                            let calendar = NSCalendar.currentCalendar()
                            let components = calendar.components([.Day,.Month,.Year,.Hour,.Minute], fromDate: date)
                            let hour = String(format: "%02d", components.hour)
                            let minutes = String(format: "%02d", components.minute)
                            let time = "\(hour):\(minutes)"
                            let day = components.day
                            let month = components.month
                            let year = components.year
                            a_case.fulldate = date
                            a_case.date = day
                            a_case.month = month
                            a_case.year = year
                            a_case.time = time
                        }
        
                        a_case.latitude = Double(latitude)
                        a_case.longitude = Double(longitude)
                        a_case.toCrime = crime
                        case_set.addObject(a_case)
                    }
                    crime.toCases = case_set
                }
                sqlite3_finalize(queryStatement2)
            }
            print("Crimes and cases downloaded.")
            self.saveContext()
        }
        sqlite3_finalize(queryStatement)
    }
    
//    func initPlaceEntity(db: COpaquePointer!) {
//        let queryStatementString = "SELECT DISTINCT Block,\"Location Description\" FROM Crimes_2015;"
//        var queryStatement: COpaquePointer = nil
//        var place_id = 1
//        if sqlite3_prepare_v2(db, queryStatementString, -1, &queryStatement, nil) == SQLITE_OK {
//            while sqlite3_step(queryStatement) == SQLITE_ROW {
//                
//                let queryResultCol1 = sqlite3_column_text(queryStatement, 0)
//                let queryResultCol2 = sqlite3_column_text(queryStatement, 1)
//                let block = String.fromCString(UnsafePointer<CChar>(queryResultCol1))!
//                let location_description = String.fromCString(UnsafePointer<CChar>(queryResultCol2))!
//                let place_entity = NSEntityDescription.entityForName("Place", inManagedObjectContext: managedObjectContext)
//                let place = NSManagedObject(entity: place_entity!, insertIntoManagedObjectContext: managedObjectContext) as! Place
//                place.block = block
//                place.location_description = location_description
//                place.id = String(place_id)
//                place_id += 1
//                let case_set = NSMutableSet()
//                
//                var queryStatement2: COpaquePointer = nil
//                let queryCases = "SELECT \"Case Number\" FROM Crimes_2015 WHERE Block=\""+block+"\" AND \"Location Description\"=\""+location_description+"\";"
//                if sqlite3_prepare_v2(db, queryCases, -1, &queryStatement2, nil) == SQLITE_OK {
//                    while sqlite3_step(queryStatement2) == SQLITE_ROW {
//                        let queryCaseCol1 = sqlite3_column_text(queryStatement2, 0)
//                        let case_number = String.fromCString(UnsafePointer<CChar>(queryCaseCol1))!
//                        
//                        let fetchRequest = NSFetchRequest(entityName: "Case")
//                        let predicate = NSPredicate(format: "id contains %@", case_number)
//                        fetchRequest.predicate = predicate
//                        do{
//                            let fetchResults = try managedObjectContext.executeFetchRequest(fetchRequest) as! [Case]
//                            for a_case in fetchResults{
//                                a_case.toPlace = place
//                                case_set.addObject(a_case)
//                            }
//                        }catch{
//                            abort()
//                        }
//                    }
//                }
//                place.toCases = case_set
//                sqlite3_finalize(queryStatement2)
//            }
//            print("Places downloaded")
//            self.saveContext()
//        }
//        sqlite3_finalize(queryStatement)
//    }

    
    func read_test()
    {
        let fetchRequest = NSFetchRequest(entityName: "Crime")
        
        do{
            let fetchResults = try managedObjectContext.executeFetchRequest(fetchRequest) as! [Crime]
            print(fetchResults.count)
//            for crime in fetchResults{
//                print(crime.crime_number!+","+crime.type!+","+crime.crime_description!)
//                if let cset = crime.toCases{
//                    for acase in cset{
//                        print(acase.id)
//                    }
//                }
//            }
            
        }catch{
            print("error")
        }

    }
    
    func sqLiteToCD()
    {
        if let db_path = NSBundle.mainBundle().pathForResource("Crimes_2015", ofType: "sqlite"){
            var db: COpaquePointer = nil
            if sqlite3_open(db_path, &db) == SQLITE_OK {
                print("Database opened")
               
                // Create Crime and Case Entity
                initCrimeCaseEntity(db)
                
                // Create Place Entity
//                initPlaceEntity(db)
            }
            else{
                print("Failed to open Database")
            }
        }
    }

}

