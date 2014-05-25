package dk.aau.student.runapp;

import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolylineOptions;
import com.google.maps.android.PolyUtil;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.app.DialogFragment;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.os.Handler;
import android.util.Log;
import android.widget.Toast;

public class RunProgress extends Activity 
{
	private Matchmaker matchmaker;
    private GoogleMap googleMap;
    private String data;
    private JSONObject route;
    private JSONArray waypoints;
    private String polyline;
    private GPSTracker gps;
    private List<LatLng> decodedRoute;
    private Marker opponent_position = null;
    private Handler read;
    
    
    @Override
    protected void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fragment_run_progress); 

        initializeMap();
        
        data = getIntent().getExtras().getString("route");
        
        drawMap();
        
        //Start matchmaking
        matchmaker = new Matchmaker();
        int route_id;
        JSONObject queue_data = null;
		try 
		{
			route_id = route.getInt("id");
	        queue_data = new JSONObject();
	        queue_data.put("route_id", route_id);
		} 
		catch (JSONException e1) 
		{
			matchmaker.close_socket();
			finish();
		}

        Message enqueue = new Message("queue", UserInfo.get_instance().get_id(), queue_data);
        matchmaker.add_message(enqueue);
        
        //Start GPS tracker
       gps = new GPSTracker(this.getApplication(), this.googleMap, this.matchmaker);
        
        //Get received messages. Called once every second
        read = new Handler();
        read.post(create_input_listener());
              
    }
   
    protected void onDestroy()
    {
    	super.onDestroy();
    	matchmaker.close_socket();
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
    
    private void drawMap()
    {
        try 
        {
			route = new JSONObject(data);
			waypoints = route.getJSONArray("waypoints");
			polyline = route.getString("polyline");
			
			
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
			}
					
			decodedRoute = PolyUtil.decode(polyline);
			googleMap.addPolyline(new PolylineOptions().addAll(decodedRoute).color(Color.argb(255, 101, 169, 234)));
			
		} 
        catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }

    //Pop-up to allow user to accept or decline a match
	public class AcceptMatchFragment extends DialogFragment {
	    @Override
	    public Dialog onCreateDialog(Bundle savedInstanceState) {
	        // Use the Builder class for convenient dialog construction
	        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
	        builder.setMessage(R.string.dialog_accept_match)
	               .setPositiveButton(R.string.accept, new DialogInterface.OnClickListener() 
	               {
	                   public void onClick(DialogInterface dialog, int id) 
	                   {
	                	   Message accept = new Message("accept", UserInfo.get_instance().get_id(), null);
	                	   matchmaker.add_message(accept);
	                   }
	               })
	               .setNegativeButton(R.string.decline, new DialogInterface.OnClickListener() 
	               {
	                   public void onClick(DialogInterface dialog, int id) 
	                   {
	                	   Intent intent = new Intent(getBaseContext(), MatchComp.class);
	                	   startActivity(intent);
	                   }
	               });
	        // Create the AlertDialog object and return it
	        return builder.create();
	    }
	}
	
	private Runnable create_input_listener()
	{
		Runnable input_listener = new Runnable()
        {
        	@Override
        	public void run()
        	{      
        		Message input = matchmaker.get_next_message();
        		
                while(input != null)
                {               						
                    if(input.get_cmd().equals("found"))
              	 	{
              	 		AcceptMatchFragment frag = new AcceptMatchFragment();
              	 		frag.show(getFragmentManager(), "match found");
              	 	}
              	 	else if(input.get_cmd().equals("start"))
              	 	{
              	 		 new CountDownTimer(10000, 1000) 
              	 		 {
              	 		     public void onTick(long millisUntilFinished) 
              	 		     {
              	 		         Toast.makeText(getBaseContext(),"seconds remaining: " + millisUntilFinished / 1000, Toast.LENGTH_SHORT).show();
              			     }

              			     public void onFinish() 
              			     {
              			         Toast.makeText(getBaseContext(),"GO!", Toast.LENGTH_LONG).show();
              			     }
              			  }.start();
              		}
              	 	else if(input.get_cmd().equals("position"))
              	 	{

              	 		JSONObject data = input.get_data();
              	 		try 
              	 		{
							Double fraction = Double.parseDouble(data.get("completion").toString());
	             	 		LatLng opponent_coord = decodedRoute.get((int)(decodedRoute.size() * fraction)); 
	             	 		if(opponent_position == null)
	             	 		{
	                  	 		Log.d("runprogress", "opponent position");
	             	 			opponent_position = googleMap.addMarker(new MarkerOptions().position(opponent_coord));
		             	 		opponent_position.setIcon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED));
	             	 		}
	             	 		else
	             	 		{
	             	 			opponent_position.setPosition(opponent_coord);
	             	 		}
	             	 		
						} 
              	 		catch (NumberFormatException e) 
              	 		{
							// TODO Auto-generated catch block
							e.printStackTrace();
						} 
              	 		catch (JSONException e) 
              	 		{
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
              	 		
              	 	}
              	 	else if(input.get_cmd().equals("winner"))
              	 	{
              	 		try 
              	 		{
							if(input.get_data().getInt("result") != UserInfo.get_instance().get_id())
							{
								Toast.makeText(getBaseContext(), "You lost the race", Toast.LENGTH_LONG).show();
							}
							else
							{
								Toast.makeText(getBaseContext(), "YOU WON THE RACE!", Toast.LENGTH_LONG).show();
							}
						} 
              	 		catch (JSONException e) 
              	 		{
							e.printStackTrace();
						}
              	 		
              	        Intent intent = new Intent(getBaseContext(), MainActivity.class);
              	        startActivity(intent);
              	        
              	        finish();
              	 	}
                    
                    input = matchmaker.get_next_message();
                }
                
                read.postDelayed(this, 1000);
        	}
        };
        
        return input_listener;
	}

	//for testing purposes
	public GoogleMap get_map()
	{
		return googleMap;
	}
	
	//for testing purposes
	public List<LatLng> get_decoded_route()
	{
		return decodedRoute;
	}
    
}
