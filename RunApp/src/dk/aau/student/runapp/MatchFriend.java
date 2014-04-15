package dk.aau.student.runapp;

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

public class MatchFriend extends ActionBarActivity 
{
    public static final int ROUTE = 1;
    private boolean activityResultIsReturned = false;
    private String activityResult = null;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_match_friend);

        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.container, new PlaceholderFragment())
                    .commit();
        }
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.match_friend, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
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
    public static class PlaceholderFragment extends Fragment {

        public PlaceholderFragment() {
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                Bundle savedInstanceState) {
            View rootView = inflater.inflate(R.layout.fragment_match_friend, container, false);
            return rootView;
        }
    }

    public void pickroute(View view)
    {
        Intent intent = new Intent(this, PickRoute.class);
        startActivityForResult(intent, MatchFriend.ROUTE);
    }

    protected void onActivityResult(int request_code, int result_code, Intent data)
    {
    	//For testing purposes
    	activityResultIsReturned = true;
    	activityResult = data.getExtras().get("route").toString();
    	
        if(result_code == MatchFriend.RESULT_OK)
        {        	
        	//Forward route data to the RunProgress activity
            Bundle route_data = data.getExtras();
            Intent intent = new Intent (this, RunProgress.class);
            intent.putExtras(route_data);
            startActivity(intent);
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
