package dk.aau.student.runapp;

public class UserInfo 
{
	static String username = null;
	static String password = null;
	static int id;
	private static UserInfo userinfo = null;
	
	private UserInfo()
	{
		this.username = "";
		this.password = "";
		this.id = -1;		
	}
	
	static String get_username()
	{
		return username;
	}
	
	static String get_password()
	{
		return password;
	}
	
	static int get_id()
	{
		return id;
	}
	
	public void set_username(String username)
	{
		this.username = username;
	}
	
	public void set_password(String password)
	{
		this.password = password;
	}
	
	public void set_id(int id)
	{
		this.id = id;
	}
	
	public static UserInfo get_instance()
	{
		if(userinfo == null)
		{
			userinfo = new UserInfo();
		}
		
		return userinfo;
	}
}
