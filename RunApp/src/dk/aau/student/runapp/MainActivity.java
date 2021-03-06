package dk.aau.student.runapp;

import android.support.v7.app.ActionBarActivity;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.content.Intent;

public class MainActivity extends ActionBarActivity
{
    private static boolean is_authenticated = false;
    
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Log.d("Debug 1", "");

        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.container, new PlaceholderFragment())
                    .commit();
        }
        
        if(!MainActivity.is_authenticated)
        {
        	Log.d("In authentication phase", "");
            is_authenticated = true;
            new Thread(new Runnable()
            {
                public void run()
                {
                	Log.d("in new thread", "");
                    if(!HttpHandler.login_request())
                    {
                       is_authenticated = false;
                       Log.d("auth failed!", "herp");                    
                    }
                    else
                    {
                        PickRoute.routes = HttpHandler.route_request();
                        Log.d("routes", PickRoute.routes.toString());
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

    /**
     * A placeholder fragment containing a simple view.
     */
    public static class PlaceholderFragment extends Fragment
    {
        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                Bundle savedInstanceState) {
            View rootView = inflater.inflate(R.layout.fragment_main, container, false);
            return rootView;
        }
    }

    /* Called when the user presses the RUN button */
    public void runOptions (View view)
    {
        Intent intent = new Intent(this, RunOptions.class);
        startActivity(intent);
    }

}
