package com.gpstracking.app;

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
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends ActionBarActivity {



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.container, new PlaceholderFragment())
                    .commit();
        }
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
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
            View rootView = inflater.inflate(R.layout.fragment_main, container, false);

            //Locals
            Button btnLocation;
            //final GPSTracker gps;

            btnLocation = (Button) rootView.findViewById(R.id.locationBtn);
            btnLocation.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    Toast.makeText(getActivity().getApplicationContext(),"No GPS",200);
                    GPSTracker gps = new GPSTracker(getActivity().getApplicationContext());
                    AccelerometerTracker accelerometer = new AccelerometerTracker(getActivity().getApplicationContext());
                    //accelerometer.getAccelerometer();

                    if(gps.canGetLocation){
                        double lat = gps.getLatitude();
                        double lon = gps.getLongitude();

                        Toast.makeText(getActivity().getApplicationContext(),"lat: " + lat + "\n" +"long: " + lon,200).show();

                    }
                    else {
                        Toast.makeText(getActivity().getApplicationContext(),"No GPS",200).show();
                    }
                }
            });
            return rootView;
        }
    }

}
