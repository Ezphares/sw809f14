package dk.aau.student.runapp;

import org.apache.http.message.BasicNameValuePair;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.content.Intent;

public class MainActivity extends ActionBarActivity
{
    private static boolean is_authenticated = false;
    
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        
        if(!MainActivity.is_authenticated)
        {
        	Log.d("In authentication phase", "");
            is_authenticated = true;
            new Thread(new Runnable()
            {
                public void run()
                {
                    BasicNameValuePair username = new BasicNameValuePair("username", "test");
                    BasicNameValuePair password = new BasicNameValuePair("password", "123456");
                    
                    if(!HttpHandler.login_request(username, password))
                    {
                       is_authenticated = false;
                       Log.d("auth failed!", "herp");                    
                    }
                    else
                    {
                        PickRoute.routes = HttpHandler.route_request();
                    }
                }
            }).start();
        }

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item)
    {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    /*

    public static class PlaceholderFragment extends Fragment
    {
        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                Bundle savedInstanceState) {
            View rootView = inflater.inflate(R.layout.fragment_main, container, false);
            return rootView;
        }
    }
    */

    /* Called when the user presses the RUN button */
    public void runOptions (View view)
    {
        Intent intent = new Intent(this, RunOptions.class);
        startActivity(intent);
    }
    
    public boolean is_authenticated()
    {
    	return is_authenticated;
    }

}
