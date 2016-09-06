//
//  Van+CoreDataProperties.swift
//  IITEscortApp
//
//  Created by Jiranun Jiratrakanvong on 7/27/16.
//  Copyright © 2016 Jiranun Jiratrakanvong. All rights reserved.
//
//  Choose "Create NSManagedObject Subclass…" from the Core Data editor menu
//  to delete and recreate this implementation file for your updated model.
//

import Foundation
import CoreData

extension Van {

    @NSManaged var time: String?
    @NSManaged var riders: NSSet?

}
