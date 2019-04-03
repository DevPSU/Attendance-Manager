package com.example.easyin;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;



import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

public class StartupActivity extends AppCompatActivity implements HTTPPostRequest.HttpReq
{
    private Context context;
    private EditText email;
    private EditText password;
    private Button loginBtn;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_startup);
        context=this;
        email=findViewById(R.id.email);
        password=findViewById(R.id.password);
        loginBtn = (Button) findViewById(R.id.loginBtn);
        loginBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                String emailS= email.getText().toString();
                String passwordS=password.getText().toString();

                JSONObject data= new JSONObject();
                try {
                    data.put("email", emailS);
                    data.put("password", passwordS);
                    data.put("should_expire", 1);


                } catch (JSONException e) {
                    e.printStackTrace();
                }
                HTTPPostRequest request = new HTTPPostRequest(context, "http://cantaloupe-dev.us-east-1.elasticbeanstalk.com/auth/login", data);

                request.execute();
                loginBtn.setClickable(false);



            }
        });
    }


    @Override
    public void login(String json)
    {
        try {
            JSONObject jsonObject=new JSONObject(json);
            if(jsonObject.has("bearer_token")){
                Intent gotoLogin = new Intent(getApplicationContext(), GymsActivity.class);
                loginBtn.setClickable(true);
                startActivity(gotoLogin);
            }
            else{
                Toast.makeText(getApplicationContext(),jsonObject.getString("error"),Toast.LENGTH_LONG).show();
                loginBtn.setClickable(true);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
        System.out.print("Login : " + json);
    }
}
