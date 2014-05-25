package dk.aau.student.runapp;

import org.json.JSONException;
import org.json.JSONObject;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;


/**
 * Created by Henrik on 09-04-14.
 */
public class GPSTracker extends Service implements LocationListener {

    private final Context mContext;
    private GoogleMap googleMap;
    private Marker currentLocation;
    public Matchmaker matchmaker;

    // flag for GPS status
    boolean isGPSEnabled = false;

    // flag for network status
    boolean isNetworkEnabled = false;

    boolean canGetLocation = false;

    double latitude; // latitude
    double longitude; // longitude

    // The minimum distance to change Updates in meters
    private static final long MIN_DISTANCE_CHANGE_FOR_UPDATES = 0; // As fast as possible

    // The minimum time between updates in milliseconds
    private static final long MIN_TIME_BW_UPDATES = 0; // As fast as possible

    // Declaring a Location Manager
    protected LocationManager locationManager;

    public GPSTracker(Context context, GoogleMap map, Matchmaker matchmaker) {
    	this.matchmaker = matchmaker;
        this.mContext = context;
        this.googleMap = map;
        getLocation();
    }
    public Location getLocation() {
        try {
            locationManager = (LocationManager) mContext
                    .getSystemService(LOCATION_SERVICE);

            // getting GPS status
            isGPSEnabled = locationManager
                    .isProviderEnabled(LocationManager.GPS_PROVIDER);

            // getting network status
            isNetworkEnabled = locationManager
                    .isProviderEnabled(LocationManager.NETWORK_PROVIDER);

            if (!isGPSEnabled) 
            {
            	stopSelf();
            } 
            else 
            {
                this.canGetLocation = true;
                // if GPS Enabled get lat/long using GPS Services
	            locationManager.requestLocationUpdates(
	                    LocationManager.GPS_PROVIDER,
	                    MIN_TIME_BW_UPDATES,
	                    MIN_DISTANCE_CHANGE_FOR_UPDATES, this);
	            Log.d("GPS Enabled", "GPS Enabled");
                    

            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        
        return null;
    }

    //Default overrides.
    @Override
    public void onLocationChanged(Location location) 
    {
    	latitude = location.getLatitude();
    	longitude = location.getLongitude();
		LatLng latlng = new LatLng(latitude, longitude);
    	
    	//CODE HERE!
    	Log.d("GPS", Double.toString(latitude) + "      " + Double.toString(longitude));

    	JSONObject data = new JSONObject();
    	try 
    	{
			data.put("lat", latitude);
	    	data.put("lng", longitude);
		} 
    	catch (JSONException e) 
    	{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    	Message msg = new Message("position", UserInfo.get_instance().get_id(), data);
    	this.matchmaker.add_message(msg);
   	
    	if(currentLocation == null) {
    		currentLocation = googleMap.addMarker(new MarkerOptions().position(latlng));
			currentLocation.setIcon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN));
    	}
    	else {

    		currentLocation.setPosition(latlng);
			//googleMap.moveCamera(CameraUpdateFactory.newLatLng(latlng));
    	}
    }

    @Override
    public void onProviderDisabled(String provider) {
    }

    @Override
    public void onProviderEnabled(String provider) {
    }

    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {
    }

    @Override
    public IBinder onBind(Intent arg0) {
        return null;
    }

    /**
     * Function to get latitude returns 0.0 on fault
     * */
    public double getLatitude(){
        // return latitude
        return latitude;
    }

    /**
     * Function to get longitude
     * */
    public double getLongitude(){
        // return longitude
        return longitude;
    }

    /**
     * Stop using GPS listener
     * Calling this function will stop using GPS in your app
     * */
    public void stopUsingGPS(){
        if(locationManager != null){
            locationManager.removeUpdates(GPSTracker.this);
        }
    }
    
}
