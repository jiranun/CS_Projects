//
//  QueryManager.swift
//  IITEscortApp
//
//  Created by Jiranun Jiratrakanvong on 7/27/16.
//  Copyright © 2016 Jiranun Jiratrakanvong. All rights reserved.
//

import Foundation

import UIKit
import CoreData

class QueryManager {
//    static var conditions = [String:String]()
    static var moc:NSManagedObjectContext?
    static var isInit = false
    
    init(){
        if (QueryManager.isInit == false){
            let appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
            QueryManager.moc = appDelegate.managedObjectContext
            QueryManager.isInit = true
        }
    }
    
    func getReservedSeat(name:String)->[String]?{
        let fetchRequest = NSFetchRequest(entityName: "Student")
        let predicate = NSPredicate(format: "name == %@", name)
        fetchRequest.predicate = predicate
        do {
            if let moc = QueryManager.moc{
                let fetchResult = try moc.executeFetchRequest(fetchRequest) as! [Student]
                if fetchResult.count > 0{
                    let passenger = fetchResult[0]
                    if let van = passenger.van{
                        return [name, van.time!, passenger.from!, passenger.to!]
                    }
                }
            }
        }catch{
            print("Fetching data error!")
        }
        return nil
    }
    
    func clearAll()->Bool{
        if let moc = QueryManager.moc{
            var success = true
            let fetchRequest = NSFetchRequest(entityName: "Van")
            fetchRequest.returnsObjectsAsFaults = false
            
            do
            {
                let results = try moc.executeFetchRequest(fetchRequest) as! [Van]
                for van in results
                {
                    let managedObjectData:NSManagedObject = van as NSManagedObject
                    moc.deleteObject(managedObjectData)
                }
            } catch let error as NSError {
                print("Delete all data error : \(error) \(error.userInfo)")
                success = false
            }
            
            let fetchRequest2 = NSFetchRequest(entityName: "Student")
            fetchRequest2.returnsObjectsAsFaults = false
            
            do
            {
                let results = try moc.executeFetchRequest(fetchRequest2) as! [Student]
                for s in results
                {
                    let managedObjectData:NSManagedObject = s as NSManagedObject
                    moc.deleteObject(managedObjectData)
                }
            } catch let error as NSError {
                print("Detele all data error : \(error) \(error.userInfo)")
                success = false
            }
            self.saveContext()
            return success
        }
        return false
    }
    
    func getVan(time:String)->Van?{
        let fetchRequest = NSFetchRequest(entityName: "Van")
        let predicate = NSPredicate(format: "time == %@", time)
        fetchRequest.predicate = predicate
        do {
            if let moc = QueryManager.moc{
                let fetchResult = try moc.executeFetchRequest(fetchRequest) as! [Van]
                if fetchResult.count > 0{
                    return fetchResult[0]
                }
            }
        }catch{
            print("Fetching data error!")
        }
        return nil

    }
    
    func getStudents(time:String)->[Student]{
        if let van = getVan(time){
            if let students = van.riders{
                var studentlist = [Student]()
                for s in students{
                    studentlist.append(s as! Student)
                }
                return studentlist
            }
        }
        return [Student]()
    }
    
    func removeStudent(name:String)->Bool{
        let fetchRequest = NSFetchRequest(entityName: "Student")
        let predicate = NSPredicate(format: "name == %@", name)
        fetchRequest.predicate = predicate
        do {
            if let moc = QueryManager.moc{
                let fetchResult = try moc.executeFetchRequest(fetchRequest) as! [Student]
                if fetchResult.count > 0{
                    let passenger = fetchResult[0]
                    let managedObjectData:NSManagedObject = passenger as NSManagedObject
                    moc.deleteObject(managedObjectData)
                    return true
                }
            }
        }catch{
            print("Removing data error!")
        }
        return false

    }
    
    func saveContext(){
        let appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
        appDelegate.saveContext()
    }
    
    func addStudent(username:String, time:String, from:String, to:String){
        if let managedObjectContext = QueryManager.moc{
            let student_entity = NSEntityDescription.entityForName("Student", inManagedObjectContext: managedObjectContext)
            let student = NSManagedObject(entity: student_entity!, insertIntoManagedObjectContext: managedObjectContext) as! Student
            student.name = username
            student.from = from
            student.to = to
            
            var a_van:Van? = nil
            
            if let van = getVan(time){
                a_van = van
            }else{
                if let managedObjectContext = QueryManager.moc{
                    let van_entity = NSEntityDescription.entityForName("Van", inManagedObjectContext: managedObjectContext)
                    let new_van = NSManagedObject(entity: van_entity!, insertIntoManagedObjectContext: managedObjectContext) as! Van
                    new_van.time = time
                    a_van = new_van
                }
            }
            if let v = a_van{
                student.van = v
                v.mutableSetValueForKey("riders").addObject(student)
            }
            self.saveContext()
        }
    }
    
//    func getMonthName(month_num:String)->String{
//        let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
//        if let mnum = Int(month_num){
//            if mnum >= 1 && mnum <= 12{
//                return months[mnum-1]
//            }
//        }
//        return ""
//    }
//    
//    func getMonthNum(month_name:String)->String{
//        let months = ["January":"1", "February":"2", "March":"3", "April":"4", "May":"5", "June":"6", "July":"7", "August":"8", "September":"9", "October":"10", "November":"11", "December":"12"]
//        if let mnum = months[month_name]{
//            return mnum
//        }
//        return ""
//    }
//    
//    func addCondition(category:String, condition:String){
//        removeCondition(category)
//        if condition == "N/A"{
//            QueryManager.conditions[category] = "0"
//        }
//        else{
//            if category == "Month"{
//                QueryManager.conditions[category] = self.getMonthNum(condition)
//            }
//            else{
//                QueryManager.conditions[category] = condition
//            }
//        }
//    }
//    
//    func removeCondition(category:String = ""){
//        if category == ""{
//            QueryManager.conditions.removeAll(keepCapacity: true)
//        }
//        else{
//            if QueryManager.conditions[category] != nil {
//                QueryManager.conditions.removeValueForKey(category)
//            }
//        }
//        //        print(QueryManager.conditions)
//    }
//    
//    func getCase(inp_case_id:String = "")->Case?{
//        var case_id = inp_case_id
//        if case_id == ""{
//            if let case_id_cond = QueryManager.conditions["Case ID"]{
//                case_id = case_id_cond
//            }
//        }
//        
//        let fetchRequest = NSFetchRequest(entityName: "Case")
//        let predicate = NSPredicate(format: "id == %@", case_id)
//        fetchRequest.predicate = predicate
//        do {
//            if let moc = QueryManager.moc{
//                let fetchResult = try moc.executeFetchRequest(fetchRequest) as! [Case]
//                let result = fetchResult[0]
//                return result
//            }
//        }catch{
//            print("Fetching data error!")
//        }
//        return nil
//    }
//    
//    func getCurrentFetchRequest() -> NSFetchRequest?{
//        let fetchRequest = NSFetchRequest(entityName: "Case")
//        
//        if let case_id = QueryManager.conditions["Case ID"]{
//            let predicate = NSPredicate(format: "id == %@", case_id)
//            fetchRequest.predicate = predicate
//            return fetchRequest
//        }
//        
//        var predicates = [NSPredicate]()
//        
//        if let case_date = QueryManager.conditions["Day"]{
//            let predicate = NSPredicate(format: "date == %@", case_date)
//            predicates.append(predicate)
//        }
//        
//        if let case_date = QueryManager.conditions["Month"]{
//            let predicate = NSPredicate(format: "month == %@", case_date)
//            predicates.append(predicate)
//        }
//        
//        if let case_date = QueryManager.conditions["Year"]{
//            let predicate = NSPredicate(format: "year == %@", case_date)
//            predicates.append(predicate)
//        }
//        
//        if let crime_number = QueryManager.conditions["IUCR Code"]{
//            let predicate = NSPredicate(format: "toCrime.crime_number == %@", crime_number)
//            predicates.append(predicate)
//        }
//        
//        if let crime_type = QueryManager.conditions["Crime Type"]{
//            let predicate = NSPredicate(format: "toCrime.type == %@", crime_type)
//            predicates.append(predicate)
//        }
//        
//        if let crime_des = QueryManager.conditions["Crime Description"]{
//            let predicate = NSPredicate(format: "toCrime.crime_description == %@", crime_des)
//            predicates.append(predicate)
//        }
//        
//        let comp_predicate = NSCompoundPredicate(type: .AndPredicateType, subpredicates: predicates)
//        fetchRequest.predicate = comp_predicate
//        return fetchRequest
//        
//    }
//    
//    // categories = ["Case Date","Case Month","Case Year", "IUCR Code", "Crime Type", "Crime Description"]
//    func getConditions(category:String, order:String = "↑")->[String]{
//        var returnStrLst = [String]()
//        if let fetchRequest = getCurrentFetchRequest(){
//            fetchRequest.returnsDistinctResults = true
//            fetchRequest.resultType = .DictionaryResultType
//            let order_b = (order=="↑")
//            var key = ""
//            switch category {
//            case "Day":
//                key = "date"
//            case "Month":
//                key = "month"
//            case "Year":
//                key = "year"
//            case "IUCR Code":
//                key = "toCrime.crime_number"
//            case "Crime Type":
//                key = "toCrime.type"
//            case "Crime Description":
//                key = "toCrime.crime_description"
//            default:
//                key = "id"
//            }
//            
//            fetchRequest.sortDescriptors = [NSSortDescriptor(key: key, ascending: order_b)]
//            fetchRequest.propertiesToFetch = [key]
//            
//            do {
//                if let moc = QueryManager.moc{
//                    let fetchResult = try moc.executeFetchRequest(fetchRequest) as! [NSDictionary]
//                    //                    let distinct = NSSet(array: fetchResult.map { $0.key })
//                    for distict_case in fetchResult as Array<NSDictionary> {
//                        if (key == "date" || key == "month" || key == "year"){
//                            if let val = distict_case.valueForKey(key) as? Int{
//                                if val == 0{
//                                    returnStrLst.append("N/A")
//                                }
//                                else{
//                                    var str = String(val)
//                                    if key == "month"{
//                                        str = self.getMonthName(str)
//                                    }
//                                    returnStrLst.append(str)
//                                }
//                            }
//                        } else {
//                            if let str = distict_case.valueForKey(key) as? String{
//                                returnStrLst.append(str)
//                            }
//                        }
//                    }
//                }
//            } catch {
//                print("Fetch result error!")
//            }
//        }
//        return returnStrLst
//    }
}