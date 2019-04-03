package com.example.easyin;

import java.io.Serializable;

public class Course implements Serializable
{
    private String courseName;
    private String courseSetting;
    private String courseInstructor;

    public Course(String name, String setting, String instructor)
    {
        courseName = name;
        courseSetting = setting;
        courseInstructor = instructor;
    }

    public String getCourseName() {
        return courseName;
    }

    public String getCourseSetting() {
        return courseSetting;
    }

    public String getCourseInstructor() {
        return courseInstructor;
    }
}
