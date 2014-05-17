package dk.aau.student.runapp;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
import java.util.concurrent.ConcurrentLinkedQueue;

import org.json.JSONException;
import org.json.JSONObject;

import android.util.Log;

public class Matchmaker 
{
	private static String IP = "192.168.0.102";
	private static int port = 8001;
	private String header = "";
	private String message = "";
	private int remaining = 0;
	private BufferedReader input;
	private DataOutputStream output;
	private ConcurrentLinkedQueue<Message> received_queue;
	private ConcurrentLinkedQueue<Message> outbound_queue;
	private Socket socket;
	
	public Matchmaker()
	{
		outbound_queue = new ConcurrentLinkedQueue<Message>();
		received_queue = new ConcurrentLinkedQueue<Message>();
		
	    new Thread(new Runnable()
	    {
	        public void run()
	        {
	        	socket = new Socket();
	        	SocketAddress sockaddr = new InetSocketAddress(IP, port);
	        	try 
	        	{	      		
					socket.connect(sockaddr);
					socket.setSoTimeout(1000);
					
					input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
					output = new DataOutputStream(socket.getOutputStream());
					
					while(socket.isConnected())
					{
						
						listen();	
						while(!outbound_queue.isEmpty())
						{
							send_message();
						}
					}
				} 
	        	catch (IOException e) 
	        	{
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
	        }
	    }).start();	    
	}
	
	public void listen()
	{
		
		if(remaining == 0)
		{
			while(header.length() < 2)
			{
				int t;
				try 
				{
					t = input.read();
					if(t == -1)
					{
						break;
					}
					else
					{
						header += (char) t;
					}								

				} 
				catch (IOException e) 
				{
					break;
				}
			}
			if(header.length() == 2)
			{
				remaining = ((int)header.charAt(0))*256 + ((int)header.charAt(1));
				message = "";
			}
		}
		else
		{
			while(remaining > 0)
			{
				int t;
				try 
				{
					t = input.read();
					if(t == -1)
					{
						break;
					}
					else
					{
						message += (char) t;
						remaining--;
					}

				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
			
			if(remaining  == 0)
			{
				try 
				{
					JSONObject temp_obj;
					temp_obj = new JSONObject(message);
					Message received_message = new Message(temp_obj);
					received_queue.add(received_message);		
					header = "";
				} 
				catch (JSONException e) 
				{
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
				
	}
	
	private void send_message()
	{
		Message msg = outbound_queue.poll();
		
		try 
		{
			output.writeUTF(msg.get_encoded());
		} 
		catch (IOException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

	Message get_next_message()
	{
		return received_queue.poll();
	}
	
	void add_message(Message msg)
	{
		outbound_queue.add(msg);
	}
	
	void close_socket()
	{
		try 
		{
			socket.close();
		} 
		catch (IOException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
