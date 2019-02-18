package com.example.easyin;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;

public class StartupActivity extends AppCompatActivity
{

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_startup);

        Button signupBtn = (Button) findViewById(R.id.signupBtn);
        signupBtn.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v) {
                String easyIn = "http://www.google.com";    //google used as place holder
                Uri webaddress = Uri.parse(easyIn);

                Intent gotoWebPage = new Intent(Intent.ACTION_VIEW, webaddress);
                if (gotoWebPage.resolveActivity(getPackageManager()) != null) {
                    startActivity(gotoWebPage);
                }
            }
        });

        Button loginBtn = (Button) findViewById(R.id.loginBtn);
        loginBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                Intent gotoLogin = new Intent(getApplicationContext(), LoginActivity.class);
                startActivity(gotoLogin);
            }
        });
    }
}
