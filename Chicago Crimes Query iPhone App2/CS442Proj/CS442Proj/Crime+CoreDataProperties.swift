//
//  Crime+CoreDataProperties.swift
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

extension Crime {

    @NSManaged var crime_description: String?
    @NSManaged var crime_number: String?
    @NSManaged var type: String?
    @NSManaged var toCases: NSSet?

}
