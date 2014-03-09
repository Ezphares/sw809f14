package dk.aau.student.runapp;

import android.app.Activity;
import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.ActionBar;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.os.Build;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

public class HTTPRequest extends Activity
{
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_httprequest);

        //Client
        HttpClient httpClient = new DefaultHttpClient();
        //Post
        HttpPost httpPost = new HttpPost("localhost:8000/login/");
        //Get
        HttpGet httpGet = new HttpGet("localhost:8000/routes/json/");

        List<NameValuePair> nameValuePair = new ArrayList<NameValuePair>(2);
        nameValuePair.add(new BasicNameValuePair("username", "test"));
        nameValuePair.add(new BasicNameValuePair("password", "123456"));

        try
        {
            httpPost.setEntity(new UrlEncodedFormEntity(nameValuePair));
        }
        catch (UnsupportedEncodingException e)
        {
            // writing error to Log
            e.printStackTrace();
        }

        try
        {
            HttpResponse response = httpClient.execute(httpPost);

            // writing response to log
            Log.d("Http Response:", response.toString());
        }
        catch (ClientProtocolException e)
        {
            // writing exception to log
            e.printStackTrace();
        }
        catch (IOException e)
        {
            // writing exception to log
            e.printStackTrace();
        }
    }

}
