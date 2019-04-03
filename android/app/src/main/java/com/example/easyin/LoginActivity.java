package com.example.easyin;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class LoginActivity extends AppCompatActivity
{
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Button loginBtn = (Button) findViewById(R.id.loginBtn);
        loginBtn.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                EditText emailEditText = (EditText) findViewById(R.id.emailEditText);
                EditText passwordEditText = (EditText) findViewById(R.id.passwordEditText);

                String userEmail = emailEditText.getText().toString();
                String userPassword = passwordEditText.getText().toString();

                TextView error = (TextView) findViewById(R.id.incorrectLoginTextView);

                if(userEmail.equals("email") && userPassword.equals("password"))
                {
                    error.setText("");

                    Intent gotoMain = new Intent(getApplicationContext(), GymsActivity.class);
                    startActivity(gotoMain);
                }
                else
                {
                    error.setText(getString(R.string.incorrect_login));
                }
            }
        });
    }

}
