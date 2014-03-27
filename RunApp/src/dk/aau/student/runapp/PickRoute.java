package dk.aau.student.runapp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class PickRoute extends Activity
{
    public static JSONArray routes;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pick_route);

        JsonList(routes);

        final ListView route_list = (ListView)findViewById(R.id.list);
        AdapterView.OnItemClickListener listener = new AdapterView.OnItemClickListener()
        {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int pos, long id)
            {
                try
                {
                    Bundle result_bundle = new Bundle();
                    
                    JSONObject selected_route = routes.getJSONObject(pos);
                    String selected_route_object = selected_route.toString();
                    result_bundle.putString("route", selected_route_object);
                                       
                    Intent resultIntent = new Intent();
                    resultIntent.putExtras(result_bundle);
                    
                    setResult(MatchComp.ROUTE, resultIntent);
                    finish();

                }
                catch (JSONException ex)
                {
                    //TODO: handle
                    return;
                }

            }
        };

        route_list.setOnItemClickListener(listener);
    }

    public void JsonList(JSONArray array)
    {
        ListView route_list = (ListView)findViewById(R.id.list);
        RouteListAdapter adapter = new RouteListAdapter(this, array);
        route_list.setAdapter(adapter);
    }

}
