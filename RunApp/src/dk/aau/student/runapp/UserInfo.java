package dk.aau.student.runapp;

public class UserInfo 
{
	public String username = null;
	public String password = null;
	public int id;
	private static UserInfo userinfo = null;
	
	private UserInfo()
	{
		this.username = "";
		this.password = "";
		this.id = -1;		
	}
	
	public String get_username()
	{
		return this.username;
	}
	
	public String get_password()
	{
		return this.password;
	}
	
	public int get_id()
	{
		return this.id;
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
