package dk.aau.student.runapp;

import org.json.JSONException;
import org.json.JSONObject;

import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

public class MatchComp extends ActionBarActivity
{
    public static final int ROUTE = 1;
    private boolean activityResultIsReturned = false;
    private String activityResult = null;
    Bundle route_data;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_match_comp);

        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.container, new PlaceholderFragment())
                    .commit();
        }
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.matchmake, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item)
    {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings)
        {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    /**
     * A placeholder fragment containing a simple view.
     */
    public static class PlaceholderFragment extends Fragment
    {

        public PlaceholderFragment()
        {
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                Bundle savedInstanceState)
        {
            View rootView = inflater.inflate(R.layout.fragment_match_comp, container, false);
            return rootView;
        }
    }

    public void pickroute(View view)
    {
        Intent intent = new Intent(this, PickRoute.class);
        startActivityForResult(intent, MatchComp.ROUTE);
    }

    public void matchmake(View view)
    {
    	Intent intent = new Intent(this, RunProgress.class);
    	intent.putExtras(route_data);
    	startActivity(intent);
    }
    protected void onActivityResult(int request_code, int result_code, Intent data)
    {
    	String name = null;
    	String r_data = (String) data.getExtras().get("route");
    	JSONObject route = null;
		try {
			route = new JSONObject(r_data);
			name = route.getString("name");
		} 
		catch (JSONException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    	
    	//For testing purposes
    	activityResultIsReturned = true;
    	activityResult = route.toString();

    	
        if(result_code == MatchComp.RESULT_OK)
        {        	
        	//Forward route data to the Matchmaking activity
            route_data = data.getExtras();
            Toast.makeText(getApplicationContext(), "Chosen route: " + name, Toast.LENGTH_LONG).show();
        }        
    }
    
    public String getActivityResult()
    {
    	return activityResult;
    }
    
    public boolean getActivityResultIsReturned()
    {
    	return activityResultIsReturned;
    }

}
