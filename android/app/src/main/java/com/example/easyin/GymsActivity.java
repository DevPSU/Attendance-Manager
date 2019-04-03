package com.example.easyin;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import java.util.ArrayList;


public class GymsActivity extends AppCompatActivity {
    static ArrayList<Course> mCourses = new ArrayList<>();

    public static RecyclerViewAdapter adapter=null;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gyms);
        mCourses.clear();
        if(adapter!=null) {
            adapter.notifyDataSetChanged();
        }
        initClasses();
        /*
        initLocation();
        HttpURLConnection.setFollowRedirects(true);
        if(mLocation != null)
        {
            //make get request
            String urlString = "https://api.yelp.com/v3/businesses/search?latitude=" + mLocation.getLatitude()
                    + "&longitude=" + mLocation.getLongitude()
                    + "&radius=8045&limit=10&categories=gyms";
            HttpGetRequest requester = new HttpGetRequest();
            requester.execute(urlString);
        }
        */

        //create recyclerview
        RecyclerView recyclerView = findViewById(R.id.recycler_view);
//        recyclerView.removeAllViewsInLayout();

        adapter = new RecyclerViewAdapter(this, mCourses);

        recyclerView.setAdapter(adapter);

        recyclerView.setLayoutManager(new LinearLayoutManager(this));
    }

    private void initClasses()
    {
        mCourses.add(new Course("Chem 110: Intro to Chemical Principles", "MWF 10:10am - 11:00am", "John Asbury"));
        mCourses.add(new Course("Econ 102: Microeconomics", "MWF 11:15am - 12:05pm", "Dave Brown"));
    }
}