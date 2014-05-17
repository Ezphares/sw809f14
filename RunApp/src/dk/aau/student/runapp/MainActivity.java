package dk.aau.student.runapp;

import org.apache.http.message.BasicNameValuePair;

import android.support.v7.app.ActionBarActivity;
import android.text.Editable;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.DialogInterface;
import android.content.Intent;

public class MainActivity extends ActionBarActivity
{
    private static boolean is_authenticated = false;
    private boolean is_reachable = true;
    private static Handler hm;
    private Dialog myDialog;
    private Button login;
    private EditText username = null;
    private EditText password = null;
    
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        hm = new Handler() 
        {
            public void handleMessage(Message m) 
            {
            	Toast.makeText(getApplicationContext(), "Server is offline, routes unavailable", Toast.LENGTH_LONG).show();                         
            }
        };
        
        new Thread(new Runnable()
        {
            public void run()
            {
                is_reachable = HttpHandler.is_reachable();
                if(is_reachable == false)
                {
                	hm.sendEmptyMessage(0);
                }
            }
        }).start();
        
        
        if(!MainActivity.is_authenticated)
        {
        	callLoginDialog();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item)
    {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    /* Called when the user presses the RUN button */
    public void runOptions (View view)
    {
        Intent intent = new Intent(this, RunOptions.class);
        startActivity(intent);
    }
    
    public boolean is_authenticated()
    {
    	return is_authenticated;
    }
    
	private void callLoginDialog() 
    {
        myDialog = new Dialog(this);
        myDialog.setContentView(R.layout.login_form);
        myDialog.setCancelable(false);
        Button login = (Button) myDialog.findViewById(R.id.loginButton);

        username = (EditText) myDialog.findViewById(R.id.et_username);
        password = (EditText) myDialog.findViewById(R.id.et_password);
        myDialog.show();

        login.setOnClickListener(new OnClickListener()
        {
           @Override
           public void onClick(View v)
           {
               final Handler handle_fail = new Handler() 
               {
                   public void handleMessage(Message m) 
                   {
                   	Toast.makeText(getApplicationContext(), "Login failed", Toast.LENGTH_LONG).show();                         
                   }
               };

              	is_authenticated = true;
                new Thread(new Runnable()
                {
                	public void run()
                    {
                        
                        BasicNameValuePair user = new BasicNameValuePair("username", username.getText().toString());
                        BasicNameValuePair pass = new BasicNameValuePair("password", password.getText().toString());
                        UserInfo.get_instance().set_username(username.getText().toString());
                        UserInfo.get_instance().set_password(password.getText().toString());
                        
                        if(!HttpHandler.login_request(user, pass))
                        {
                        	handle_fail.sendEmptyMessage(0);
                            is_authenticated = false; 
                            runOnUiThread(new Runnable()
                            {
                            	@Override
                            	public void run()
                            	{
                            		myDialog.show();
                            	}
                            });
                        }
                        else
                        {
                            PickRoute.routes = HttpHandler.route_request();
                        }
                    }
                }).start();      
                myDialog.dismiss();
           }

                   
        });

    }   
}
