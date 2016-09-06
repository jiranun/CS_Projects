//
//  Case+CoreDataProperties.swift
//  CS442Proj
//
//  Created by Jiranun Jiratrakanvong, Kartikay Gautam on 6/27/16.
//  Copyright © 2016 Jiranun Jiratrakanvong, Kartikay Gautam. All rights reserved.
//
//  Choose "Create NSManagedObject Subclass…" from the Core Data editor menu
//  to delete and recreate this implementation file for your updated model.
//

import Foundation
import CoreData

extension Case {

    @NSManaged var date: NSNumber?
    @NSManaged var id: String?
    @NSManaged var latitude: NSNumber?
    @NSManaged var longitude: NSNumber?
    @NSManaged var fulldate: NSDate?
    @NSManaged var month: NSNumber?
    @NSManaged var year: NSNumber?
    @NSManaged var time: String?
    @NSManaged var toCrime: Crime?

}
