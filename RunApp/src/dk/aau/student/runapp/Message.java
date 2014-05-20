package dk.aau.student.runapp;

import org.json.JSONException;
import org.json.JSONObject;

public class Message 
{
	private String cmd;
	private int id;
	private JSONObject data; 
	
	public Message(String cmd, int user_id, JSONObject data)
	{
		this.cmd = cmd;
		this.id = user_id;	
		this.data = data;
	}
	
	public Message(JSONObject obj)
	{
		try 
		{
			this.cmd = obj.getString("cmd");
			
			if(obj.has("id"))
			{
				this.id = obj.getInt("id");
			}
			else
				obj.put("id", UserInfo.get_instance().get_id());

			if(obj.get("data") == JSONObject.NULL)
			{
				this.data = null;
			}
			else
			{
				this.data = obj.getJSONObject("data");
			}
		} 
		catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	private JSONObject compile()
	{
		JSONObject obj = new JSONObject();	
		try 
		{
			obj.put("cmd", cmd);
			obj.put("id", id);
			if(data == null)
			{
				obj.put("data", JSONObject.NULL);
			}
			else
			{
				obj.put("data", data);
			}
		} 
		catch (JSONException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	
		return obj;
	}
	
	public String get_encoded()
	{	
		return compile().toString();		
	}
	
	public String get_cmd()
	{
		return cmd;
	}
	
	public int get_id()
	{
		return id;
	}
	
	public JSONObject get_data()
	{
		return data;
	}

}
