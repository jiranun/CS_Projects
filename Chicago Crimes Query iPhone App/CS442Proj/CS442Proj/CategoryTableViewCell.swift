//
//  CategoryTableViewCell.swift
//  CS442Proj
//
//  Created by Jiranun Jiratrakanvong, Kartikay Gautam on 6/21/16.
//  Copyright © 2016 Jiranun Jiratrakanvong, Kartikay Gautam. All rights reserved.
//

import UIKit

class CategoryTableViewCell: UITableViewCell {

    @IBOutlet weak var cateLabel: UILabel!
    @IBOutlet weak var orderButton: UIButton!
    @IBOutlet weak var stateSwitch: UISwitch!
    var order = "↑"
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
        orderButton.setTitle(order, forState: .Normal)
    }

    @IBAction func orderChanged(sender: UIButton) {
        if order == "↑"{
            order = "↓"
        }
        else{
            order = "↑"
        }
        orderButton.setTitle(order, forState: .Normal)
        
    }
    
    override func setSelected(selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
