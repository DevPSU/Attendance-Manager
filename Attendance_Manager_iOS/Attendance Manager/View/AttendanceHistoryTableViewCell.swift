//
//  AttendanceHistoryTableViewCell.swift
//  Attendance Manager
//
//  Created by Nick Fink on 3/24/19.
//  Copyright © 2019 PSU Attendance Management Team. All rights reserved.
//

import UIKit

class AttendanceHistoryTableViewCell: UITableViewCell {

    
    @IBOutlet weak var dateLabel: UILabel!
    @IBOutlet weak var statusLabel: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
