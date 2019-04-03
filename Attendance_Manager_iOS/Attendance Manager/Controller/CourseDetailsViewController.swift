//
//  CourseDetailsViewController.swift
//  Attendance Manager
//
//  Created by Nick Fink on 3/24/19.
//  Copyright © 2019 PSU Attendance Management Team. All rights reserved.
//

import UIKit

class CourseDetailsViewController:UIViewController,UITableViewDataSource,UITableViewDelegate {
    
    var pastClasses : [String : String] = [:]
    
    @IBOutlet weak var classNameLabel: UILabel!
    @IBOutlet weak var classDateTimeLabel: UILabel!
    @IBOutlet weak var professorNameLabel: UILabel!
    @IBOutlet weak var courseHistoryTableView: UITableView!
    @IBOutlet weak var checkInButton: UIButton!
    var course : Class!
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return pastClasses.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cellIdentifier = "AttendanceHistoryTableViewCell"
        
        guard let cell = tableView.dequeueReusableCell(withIdentifier: cellIdentifier, for: indexPath) as? AttendanceHistoryTableViewCell else {
            fatalError("The dequeued cell is not an instance of AttendanceHistoryTableViewCell.")
        }
        
        let date = Array(pastClasses.keys)[indexPath.row]
        let attendance = Array(pastClasses.values)[indexPath.row]
        
        cell.statusLabel.text = attendance
        cell.dateLabel.text = date
        
        return cell
    }
    

    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        
            classNameLabel.text = course.className
            classDateTimeLabel.text = course.classMeetingDays + course.classStartTime + "-" + course.classEndTime
            professorNameLabel.text = course.professorFirstName + " " + course.professorLastName
            for (course, record) in course.attendanceHistory
            {
                pastClasses[course] = record
            }
        //courseHistoryTableView.dataSource = self ----- removed due to incompatibility with data coming from server. will need revised to function
        }
    
    

    @IBAction func checkInPressed(_ sender: Any) {
        checkInButton.setImage(UIImage(named: "checkedin-button"), for: .normal)
    }
    
    

}
