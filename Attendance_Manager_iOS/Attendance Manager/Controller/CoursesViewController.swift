//
//  CoursesViewController.swift
//  Attendance Manager
//
//  Created by Nick Fink on 2/10/19.
//  Copyright © 2019 PSU Attendance Management Team. All rights reserved.
//

import os.log
import UIKit

class CoursesViewController: UIViewController,UITableViewDataSource,UITableViewDelegate {
    
    var classes = [Class]()
    
    @IBOutlet weak var coursesTableView: UITableView!
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return classes.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
     
        let cellIdentifier = "CoursesViewCell"
        
        guard let cell = tableView.dequeueReusableCell(withIdentifier: cellIdentifier, for: indexPath) as? CoursesViewCell else {
            fatalError("The dequeued cell is not an instance of CoursesViewCell.")
        }
        
        let course = classes[indexPath.row]
        
        cell.classNameLabel.text = course.className
        cell.dateTimeLabel.text = course.classMeetingDays + course.classStartTime + "-" + course.classEndTime
        
        return cell
    }
    
    private func loadSampleClasses ()
    {
        
        
        let class1 = Class(className : "ECON 102", professorFirstName : "Kevin", professorLastName : "Johnson", classMeetingDays : "MWF", classStartTime : "11:15AM", classEndTime : "12:20PM", attendanceHistory : ["February 1st" : "Present", "February 3rd" : "Absent"])
        
        let class2 = Class(className : "CMPEN 331", professorFirstName : "Mohamed", professorLastName : "Almekkawy", classMeetingDays : "TuTh", classStartTime : "9:05AM", classEndTime : "10:20AM", attendanceHistory : ["February 2nd" : "Present", "February 4th" : "Absent"])
        
        classes += [class1, class2]
        
    }
    
    
    
    
    @IBAction func unwindToCourses(segue: UIStoryboardSegue)
    {
        
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        loadSampleClasses()
        coursesTableView.dataSource = self
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        super.prepare(for: segue, sender: sender)
        
        if segue.identifier == "ShowClassDetails"
        {
            guard let courseDetailViewController = segue.destination as? CourseDetailsViewController else
            {
                fatalError("Unexpected destination: \(segue.destination)")
            }
            guard let selectedClassCell = sender as? CoursesViewCell else {
                fatalError("Unexpected sender: \(sender)")
            }
            guard let indexPath = coursesTableView.indexPath(for: selectedClassCell) else {
                fatalError("The selected cell is not being displayed by the table")
            }
            
            let selectedClass = classes[indexPath.row]
            courseDetailViewController.course = selectedClass
        }
            
        else
        {
            fatalError("Unexpected Segue Identifier; \(segue.identifier)")
        }
    }

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
