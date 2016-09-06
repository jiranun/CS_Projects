//
//  QueryManager.swift
//  CS442Proj
//
//  Created by Jiranun Jiratrakanvong, Kartikay Gautam on 6/25/16.
//  Copyright © 2016 Jiranun Jiratrakanvong, Kartikay Gautam. All rights reserved.
//

import Foundation
import UIKit
import CoreData

class QueryManager {
    static var conditions = [String:String]()
    static var moc:NSManagedObjectContext?
    static var isInit = false
    
    init(){
        if (QueryManager.isInit == false){
            let appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
            QueryManager.moc = appDelegate.managedObjectContext
            QueryManager.isInit = true
        }
    }
    
    func getMonthName(month_num:String)->String{
        let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        if let mnum = Int(month_num){
            if mnum >= 1 && mnum <= 12{
                return months[mnum-1]
            }
        }
        return ""
    }
    
    func getMonthNum(month_name:String)->String{
        let months = ["January":"1", "February":"2", "March":"3", "April":"4", "May":"5", "June":"6", "July":"7", "August":"8", "September":"9", "October":"10", "November":"11", "December":"12"]
        if let mnum = months[month_name]{
            return mnum
        }
        return ""
    }
    
    func addCondition(category:String, condition:String){
        removeCondition(category)
        if condition == "N/A"{
            QueryManager.conditions[category] = "0"
        }
        else{
            if category == "Month"{
                QueryManager.conditions[category] = self.getMonthNum(condition)
            }
            else{
                QueryManager.conditions[category] = condition
            }
        }
    }
    
    func removeCondition(category:String = ""){
        if category == ""{
            QueryManager.conditions.removeAll(keepCapacity: true)
        }
        else{
            if QueryManager.conditions[category] != nil {
                QueryManager.conditions.removeValueForKey(category)
            }
        }
//        print(QueryManager.conditions)
    }
    
    func getCase(inp_case_id:String = "")->Case?{
        var case_id = inp_case_id
        if case_id == ""{
            if let case_id_cond = QueryManager.conditions["Case ID"]{
                case_id = case_id_cond
            }
        }
        
        let fetchRequest = NSFetchRequest(entityName: "Case")
        let predicate = NSPredicate(format: "id == %@", case_id)
        fetchRequest.predicate = predicate
        do {
            if let moc = QueryManager.moc{
                let fetchResult = try moc.executeFetchRequest(fetchRequest) as! [Case]
                let result = fetchResult[0]
                return result
            }
        }catch{
            print("Fetching data error!")
        }
        return nil
    }
    
    func getCurrentFetchRequest() -> NSFetchRequest?{
        let fetchRequest = NSFetchRequest(entityName: "Case")
        
        if let case_id = QueryManager.conditions["Case ID"]{
            let predicate = NSPredicate(format: "id == %@", case_id)
            fetchRequest.predicate = predicate
            return fetchRequest
        }
        
        var predicates = [NSPredicate]()
        
        if let case_date = QueryManager.conditions["Day"]{
            let predicate = NSPredicate(format: "date == %@", case_date)
            predicates.append(predicate)
        }
        
        if let case_date = QueryManager.conditions["Month"]{
            let predicate = NSPredicate(format: "month == %@", case_date)
            predicates.append(predicate)
        }
        
        if let case_date = QueryManager.conditions["Year"]{
            let predicate = NSPredicate(format: "year == %@", case_date)
            predicates.append(predicate)
        }
        
        if let crime_number = QueryManager.conditions["IUCR Code"]{
            let predicate = NSPredicate(format: "toCrime.crime_number == %@", crime_number)
            predicates.append(predicate)
        }
        
        if let crime_type = QueryManager.conditions["Crime Type"]{
            let predicate = NSPredicate(format: "toCrime.type == %@", crime_type)
            predicates.append(predicate)
        }
        
        if let crime_des = QueryManager.conditions["Crime Description"]{
            let predicate = NSPredicate(format: "toCrime.crime_description == %@", crime_des)
            predicates.append(predicate)
        }
        
        let comp_predicate = NSCompoundPredicate(type: .AndPredicateType, subpredicates: predicates)
        fetchRequest.predicate = comp_predicate
        return fetchRequest

    }
    
    // categories = ["Case Date","Case Month","Case Year", "IUCR Code", "Crime Type", "Crime Description"]
    func getConditions(category:String, order:String = "↑")->[String]{
        var returnStrLst = [String]()
        if let fetchRequest = getCurrentFetchRequest(){
            fetchRequest.returnsDistinctResults = true
            fetchRequest.resultType = .DictionaryResultType
            let order_b = (order=="↑")
            var key = ""
            switch category {
            case "Day":
                key = "date"
            case "Month":
                key = "month"
            case "Year":
                key = "year"
            case "IUCR Code":
                key = "toCrime.crime_number"
            case "Crime Type":
                key = "toCrime.type"
            case "Crime Description":
                key = "toCrime.crime_description"
            default:
                key = "id"
            }
            
            fetchRequest.sortDescriptors = [NSSortDescriptor(key: key, ascending: order_b)]
            fetchRequest.propertiesToFetch = [key]
            
            do {
                if let moc = QueryManager.moc{
                    let fetchResult = try moc.executeFetchRequest(fetchRequest) as! [NSDictionary]
//                    let distinct = NSSet(array: fetchResult.map { $0.key })
                    for distict_case in fetchResult as Array<NSDictionary> {
                        if (key == "date" || key == "month" || key == "year"){
                            if let val = distict_case.valueForKey(key) as? Int{
                                if val == 0{
                                    returnStrLst.append("N/A")
                                }
                                else{
                                    var str = String(val)
                                    if key == "month"{
                                        str = self.getMonthName(str)
                                    }
                                    returnStrLst.append(str)
                                }
                            }
                        } else {
                            if let str = distict_case.valueForKey(key) as? String{
                                returnStrLst.append(str)
                            }
                        }
                    }
                }
            } catch {
                print("Fetch result error!")
            }
        }
        return returnStrLst
    }
}