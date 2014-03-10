package dk.aau.student.runapp;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by Vixen on 10-03-14.
 */
public class RouteListAdapter extends BaseAdapter
{
    private JSONArray items;
    private Context context;
    private ViewGroup group;

    public RouteListAdapter(Context ctx, JSONArray array)
    {
        super();
        this.items = array;
        this.context = ctx;
    }

    public int getCount()
    {
        return items.length();
    }

    public Object getItem(int position)
    {
        return position;
    }

    public long getItemId(int position)
    {
        return position;
    }

    public View getView(int position, View convertView, ViewGroup parent)
    {
        View view = convertView;
        ViewGroup group = parent;

        if (view == null)
        {
            LayoutInflater vi = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            view = vi.inflate(R.layout.route_list, null);
            Log.d("We're in getView", "");
        }

        String itemText = "";
        String itemID = "";

        try
        {
            JSONObject jsonObject = items.getJSONObject(position);
            itemText = jsonObject.getString("name");
        }
        catch (JSONException e)
        {

        }

        if (itemText != "")
        {
            TextView name = (TextView) view.findViewById(R.id.route_name);
            ImageView image = (ImageView) view.findViewById(R.id.icon);

            if (name != null)
            {
                name.setText(itemText);
            }
        }

        return view;
    }

}