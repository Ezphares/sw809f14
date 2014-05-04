package dk.aau.student.runapp;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpRequestBase;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.util.Log;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by Vixen on 09-03-14.
 *
 */
public class HttpHandler
{
    private static HttpClient client = new DefaultHttpClient();
    private static String IP = "192.168.0.100";
    private static String test = "10.0.2.2";
    public static class ResponseData
    {
        public String body;
        public int status;
    }

    public enum HttpMethod{GET, POST}

    public static boolean is_reachable()
    {
    	SocketAddress sockaddr = new InetSocketAddress(IP, 8000);
    	// Create your socket
    	Socket socket = new Socket();
    	boolean online = true;
    	// Connect with 10 s timeout
    	try 
    	{
    	    socket.connect(sockaddr, 10000);
    	} 
    	catch (IOException iOException) 
    	{
    	    online = false;  
    	} 
    	finally 
    	{
    	    // As the close() operation can also throw an IOException
    	    // it must caught here
    	    try 
    	    {
    	        socket.close();
    	    } 
    	    catch (IOException ex) 
    	    {
    	        // feel free to do something moderately useful here, eg log the event
    	    }

    	}

    	return online;
    }
    
    public static ResponseData http_request(String url, HttpMethod method, List<NameValuePair> parameters)
    {
        //prep request
        HttpRequestBase request = null;

        if(method == HttpMethod.GET)
        {
            request = new HttpGet(url);
            //TODO: URl encode parameters

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
            HttpResponse response = client.execute(request);
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

    public static boolean login_request(BasicNameValuePair username, BasicNameValuePair password)
    {
        boolean success = false;
        
        List<NameValuePair> nameValuePair = new ArrayList<NameValuePair>(2);
        
        nameValuePair.add(username);
        nameValuePair.add(password);

        HttpHandler.ResponseData response = HttpHandler.http_request("http://" + IP + ":8000/api/login/", HttpHandler.HttpMethod.POST, nameValuePair);
        JSONObject json;
        try
        {
            json = new JSONObject(response.body);
            Log.d("login response", json.getString("status"));
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
        HttpHandler.ResponseData response = HttpHandler.http_request("http://" + IP + ":8000/api/routes/", HttpMethod.GET, null);
        JSONArray routes;
        JSONObject json;

        try
        {
            json = new JSONObject(response.body);
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
