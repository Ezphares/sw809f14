package dk.aau.student.runapp;

import android.util.Log;

import org.apache.http.HttpEntity;
import org.apache.http.HttpEntityEnclosingRequest;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpEntityEnclosingRequestBase;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpRequestBase;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by Vixen on 09-03-14.
 *
 */
public class HttpHandler
{
    public static class ResponseData
    {
        public String body;
        public int status;
    }

    public enum HttpMethod{GET, POST}

    public static ResponseData http_request(String url, HttpMethod method, List<NameValuePair> parameters)
    {
        //prep request
        HttpRequestBase request = null;
        //Client
        HttpClient httpClient = new DefaultHttpClient();

        if(method == HttpMethod.GET)
        {
            request = new HttpGet(url);


        }
        else if(method == HttpMethod.POST)
        {
            HttpPost post = new HttpPost(url);
            try
            {
                post.setEntity(new UrlEncodedFormEntity(parameters));
            }
            catch (UnsupportedEncodingException e)
            {
                e.printStackTrace();
            }

            request = post;
        }

        try
        {
            HttpResponse response = httpClient.execute(request);
            HttpEntity entity = response.getEntity();

            ResponseData data = new HttpHandler.ResponseData();
            data.body = EntityUtils.toString(entity, "UTF-8");
            data.status = response.getStatusLine().getStatusCode();

            return data;
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

        return null;
    }

    public static boolean login_request()
    {
        boolean success = false;

        List<NameValuePair> nameValuePair = new ArrayList<NameValuePair>(2);
        nameValuePair.add(new BasicNameValuePair("username", "test"));
        nameValuePair.add(new BasicNameValuePair("password", "123456"));

        HttpHandler.ResponseData response = HttpHandler.http_request("http://10.0.2.2:8000/api/login/", HttpHandler.HttpMethod.POST, nameValuePair);
        JSONObject json;
        try
        {
            json = new JSONObject(response.body);
            if(response.status == 200 && json.getString("status").equals("OK"))
            {
                success = true;
            }
        }
        catch(JSONException e)
        {
            //TODO: handle
            return false;
        }

        return success;
    }

    public static JSONArray route_request()
    {
        HttpHandler.ResponseData response = HttpHandler.http_request("http://10.0.2.2:8000/api/routes/", HttpMethod.GET, null);
        JSONArray routes;
        JSONObject json;

        try
        {
            //TODO:this object should be response.body
            String json_dummy = "{\"routes\": [{\"round_trip\": true, \"name\": \"Short Home\", \"waypoints\": [{\"lat\": 57.02523535607132, \"lng\": 9.978139400482178}, {\"lat\": 57.02533462538658, \"lng\": 9.979448318481445}, {\"lat\": 57.02795056827062, \"lng\": 9.98084306716919}, {\"lat\": 57.02554484188537, \"lng\": 9.981647729873657}]}, {\"round_trip\": true, \"name\": \"Medium Home\", \"waypoints\": [{\"lat\": 57.02527623170388, \"lng\": 9.978150129318237}, {\"lat\": 57.025328786022556, \"lng\": 9.979480504989624}, {\"lat\": 57.02795640722305, \"lng\": 9.980757236480713}, {\"lat\": 57.01968753180136, \"lng\": 9.981379508972168}]}, {\"round_trip\": true, \"name\": \"~5k\", \"waypoints\": [{\"lat\": 57.0252820710763, \"lng\": 9.978150129318237}, {\"lat\": 57.02532294665736, \"lng\": 9.979480504989624}, {\"lat\": 57.02797392407453, \"lng\": 9.981014728546143}, {\"lat\": 57.01564585861737, \"lng\": 9.99133586883545}]}]}";
            json = new JSONObject(json_dummy);
            if(response.status == 200)
            {
               routes = json.getJSONArray("routes");
               return routes;
            }
        }
        catch(JSONException ex)
        {
            //TODO: HANDLE IT!
            return null;
        }

        return null;
    }
}
