//
//  CoursesViewController.swift
//  Attendance Manager
//
//  Created by Nick Fink on 2/10/19.
//  Copyright © 2019 PSU Attendance Management Team. All rights reserved.
//

import UIKit

class CoursesViewController: UIViewController,UICollectionViewDataSource,UICollectionViewDelegate,UICollectionViewDelegateFlowLayout {
    
    
    @IBOutlet weak var CoursesCollectionView: UICollectionView!
    @IBAction func unwindToCourses(segue: UIStoryboardSegue)
    {
        
    }
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return 10
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "CourseCell", for: indexPath as IndexPath) as! CoursesCell
        cell.ClassSectionLabel.text = "Section \(indexPath.item + 1)"
        cell.backgroundColor = UIColor.white
        cell.layer.borderWidth = 1
        cell.layer.cornerRadius = 15
        cell.contentView.layer.masksToBounds = true
        cell.layer.shadowColor = UIColor.black.cgColor
        cell.layer.shadowOffset = CGSize(width: 0, height: 1.0)
        cell.layer.shadowRadius = 15.0
        cell.layer.shadowOpacity = 0.5
        cell.layer.masksToBounds = false
        cell.layer.shadowPath = UIBezierPath(roundedRect: cell.bounds, cornerRadius: cell.contentView.layer.cornerRadius).cgPath
        return cell
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        CoursesCollectionView.delegate = self
        CoursesCollectionView.dataSource = self
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
