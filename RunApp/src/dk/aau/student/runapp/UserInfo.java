package dk.aau.student.runapp;

public class UserInfo 
{
	static String username = null;
	static String password = null;
	static int id;
	private static UserInfo userinfo = new UserInfo();
	
	private UserInfo()
	{
		username = "test";
		password = "123456";
		id = 2;		
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
}
