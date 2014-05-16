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
			this.id = Integer.parseInt(obj.getString("id"));
			this.data = (JSONObject) obj.get("data");
		} 
		catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	JSONObject compile()
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
	
	String get_encoded()
	{	
		return compile().toString();		
	}

}
