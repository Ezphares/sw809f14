package dk.aau.student.runapp;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

import android.app.Activity;
import android.os.Bundle;
import android.widget.Toast;

public class RunProgress extends Activity 
{
    private GoogleMap googleMap;
    private String data;
    JSONObject route;
    JSONArray waypoints;
    GPSTracker gps;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fragment_run_progress); 

        initializeMap();
        initializeGPS();
        
        data = getIntent().getExtras().getString("route");
        try 
        {
			route = new JSONObject(data);
			waypoints = route.getJSONArray("waypoints");
			
			double start_lat = waypoints.getJSONObject(0).getDouble("lat");
			double start_lng = waypoints.getJSONObject(0).getDouble("lng");
			
			CameraUpdate center = CameraUpdateFactory.newLatLng(new LatLng(start_lat, start_lng));
			CameraUpdate zoom=CameraUpdateFactory.zoomTo(15);
		    googleMap.moveCamera(center);
		    googleMap.animateCamera(zoom);
		
			for(int i = 0; i <waypoints.length(); i++)
			{
				double lat = waypoints.getJSONObject(i).getDouble("lat");				
				double lng = waypoints.getJSONObject(i).getDouble("lng");
				googleMap.addMarker(new MarkerOptions()
		        .position(new LatLng(lat, lng)));
			}
			
		} catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        
        
        
        }
    
    /**
     * function to load map. If map is not created it will create it for you
     * */
    private void initializeMap() 
    {
        if (googleMap == null) {
        	googleMap = ((MapFragment) getFragmentManager().findFragmentById(
                    R.id.map)).getMap();
 
            // check if map is created successfully or not
            if (googleMap == null) {
                Toast.makeText(getApplicationContext(),
                        "Sorry! unable to create maps", Toast.LENGTH_SHORT)
                        .show();
            }
        }
    }
    
    private void initializeGPS()
    {
        gps = new GPSTracker(this.getApplication(), this.googleMap);
    }
 
}
