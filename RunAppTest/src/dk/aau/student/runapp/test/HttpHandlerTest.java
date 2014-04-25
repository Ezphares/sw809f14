package dk.aau.student.runapp.test;

import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;

import dk.aau.student.runapp.HttpHandler;
import junit.framework.TestCase;

public class HttpHandlerTest extends TestCase 
{
    private BasicNameValuePair username = new BasicNameValuePair("username", "test");
    private BasicNameValuePair password = new BasicNameValuePair("password", "123456");
    private BasicNameValuePair password_wrong = new BasicNameValuePair("password", "12345");
    private boolean success;
    
	public HttpHandlerTest(String name) {
		super(name);
	}

	protected void setUp() throws Exception 
	{
		super.setUp();
		success = HttpHandler.login_request(username, password);

	}
	
	public void testPrecondictions()
	{
		boolean reachable = HttpHandler.is_reachable();
		
		assertTrue(reachable);
	}

	public void test_correct_login()
	{
		assertTrue(success);	
	}
	
	/*
	 * Currently untestable because no log out functionality
	 * 
	public void test_wrong_password_login()
	{
		boolean fail = HttpHandler.login_request(username, password_wrong);
		
		assertFalse(fail);
	}
	*/
	
	public void test_route_request()
	{
		JSONArray routes = null;
		
		routes = HttpHandler.route_request();
		
		assertNotNull(routes);
	}
	
	
}
