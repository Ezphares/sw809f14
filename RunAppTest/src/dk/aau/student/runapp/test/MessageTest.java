package dk.aau.student.runapp.test;

import org.json.JSONException;
import org.json.JSONObject;

import android.util.Log;
import dk.aau.student.runapp.Message;
import junit.framework.TestCase;

public class MessageTest extends TestCase 
{
	String command;
	int id;
	JSONObject data;
	JSONObject message;
	
	

	protected void setUp() throws Exception 
	{
		super.setUp();
		
		command = "queue";
		id = 1;
		data = null;
		message  = new JSONObject();
	}
	
	public void test_message_constructor()
	{
		Message msg = new Message(command, id, null);
		
		assertEquals(msg.get_cmd(), this.command);
		assertEquals(msg.get_id(), this.id);
		assertEquals(msg.get_data(), this.data);
	}
	
	public void test_message_object_constructor()
	{
		try 
		{
			message.put("cmd", this.command);
			message.put("id", this.id);
			message.put("data", JSONObject.NULL);
		} 
		catch (JSONException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		Message msg = new Message(message);
		
		assertEquals(msg.get_cmd(), this.command);
		assertEquals(msg.get_id(), this.id);
		assertEquals(msg.get_data(), this.data);		
	}

	public void test_get_encoded()
	{
		Message msg = new Message(this.command, this.id, null);
		
		try 
		{
			message.put("cmd", this.command);
			message.put("id", this.id);
			message.put("data", JSONObject.NULL);
		} 
		catch (JSONException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		Log.d("json: ", message.toString());
		Log.d("msg: ", msg.get_encoded());
		assertEquals(message.toString(), msg.get_encoded());		
	}
}
