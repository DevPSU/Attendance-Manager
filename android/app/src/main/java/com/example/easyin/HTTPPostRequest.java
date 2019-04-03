package com.example.easyin;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class HTTPPostRequest extends AsyncTask {
    private Context mContext;
    private String response = "";
    private String strURL = "";
    private JSONObject dataObject;
    private  HttpReq httpReq;
    private String json;
    private int id = -1;
    private boolean isCoordinatesData = false;
//    private SharedDataManager sharedDataManager;
//    private static final HTTPPostRequest ourInstance = new HTTPPostRequest();
//
//    public static HTTPPostRequest getInstance() {
//        return ourInstance;
//    }

    public HTTPPostRequest(Context mContext, String strURL, JSONObject dataObject) {
        this.mContext = mContext;
        this.strURL = strURL;
        this.dataObject = dataObject;
        httpReq= (HttpReq) this.mContext;

    }

    @Override
    protected Object doInBackground(Object[] objects) {
        HttpURLConnection httpURLConnection = null;
        InputStream response = null;
        int code = 0;
        URL url;
        String status = null;
        try{
            url = new URL(strURL);
            System.out.println("URL : " + url);
            httpURLConnection = (HttpURLConnection) url.openConnection();
            httpURLConnection.setDoInput(true);
            httpURLConnection.setDoOutput(true);
            httpURLConnection.setRequestMethod("POST");
            httpURLConnection.setRequestProperty("Accept", "application/json");
            httpURLConnection.setRequestProperty("Content-Type", "application/json");
            httpURLConnection.setConnectTimeout(30000);
            httpURLConnection.setReadTimeout(30000);
            OutputStream out = httpURLConnection.getOutputStream();
            Log.e("LoginData", dataObject.toString());
            out.write(dataObject.toString().getBytes("UTF-8"));
            out.flush();
            httpURLConnection.connect();

            BufferedReader reader = null;
            code = httpURLConnection.getResponseCode();
            System.out.println("Code : "+code);
            if (httpURLConnection.getResponseCode() != 200) {
                response = httpURLConnection.getErrorStream();


            } else {
                response = httpURLConnection.getInputStream();
            }

            reader = new BufferedReader(new InputStreamReader(response, "UTF-8"));
            json = reader.readLine();
            Log.e("Reponse", "  ::  " + json);

        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    protected void onPostExecute(Object o) {
        super.onPostExecute(o);
        httpReq.login(json);
    }

    public interface HttpReq{
        void login(String json);
    }
}
