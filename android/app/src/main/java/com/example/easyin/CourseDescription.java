package com.example.easyin;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.InputStream;

public class CourseDescription extends AppCompatActivity {
    private Course mCourse;
    private TextView mCourseNameTV;
    private TextView mCourseSettingTV;
    private TextView mCourseInstructorTV;
    private Bitmap bitmap;
    private Button checkinButton;
    InputStream inputStream;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_course_description);
        mCourse= (Course) getIntent().getSerializableExtra("Course");

        mCourseNameTV = (TextView)findViewById(R.id.courseNameTV);
        mCourseSettingTV = (TextView)findViewById(R.id.courseSettingTV);
        mCourseInstructorTV = (TextView)findViewById(R.id.courseInstructorTV);
        checkinButton=findViewById(R.id.checkInButton);
        mCourseNameTV.setText(mCourse.getCourseName());
        mCourseSettingTV.setText(mCourse.getCourseSetting());
        mCourseInstructorTV.setText(mCourse.getCourseInstructor());

        final int checkedInImage=getResources().getIdentifier("checkedin_button","mipmap",getPackageName());
        checkinButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                checkinButton.setBackgroundResource(checkedInImage);
            }
        });



    }
}
