package dk.aau.student.runapp;

import android.app.Activity;
import android.app.ListActivity;
import android.app.LoaderManager;
import android.content.Context;
import android.content.Loader;
import android.database.Cursor;
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
import android.widget.Adapter;
import android.widget.ListView;
import android.widget.TextView;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.List;

public class PickRoute extends Activity
{
    public static JSONArray routes;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pick_route);
        JsonList(routes);
    }

    public void JsonList(JSONArray array)
    {
        Log.d("Calling the JsonList", "");
        ListView route_list = (ListView)findViewById(R.id.list);
        Log.d("ListView route:", route_list.toString());
        RouteListAdapter adapter = new RouteListAdapter(this, array);
        Log.d("Adapter:", adapter.toString());
        route_list.setAdapter(adapter);
    }

}
