//
//  CoursesViewCell.swift
//  Attendance Manager
//
//  Created by Nick Fink on 3/24/19.
//  Copyright © 2019 PSU Attendance Management Team. All rights reserved.
//

import UIKit

class CoursesViewCell: UITableViewCell {

    @IBOutlet weak var classNameLabel: UILabel!
    @IBOutlet weak var dateTimeLabel: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
