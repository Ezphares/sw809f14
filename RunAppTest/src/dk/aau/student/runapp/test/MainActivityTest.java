package dk.aau.student.runapp.test;

import dk.aau.student.runapp.MainActivity;
import dk.aau.student.runapp.R;
import dk.aau.student.runapp.RunOptions;
import android.app.Activity;
import android.app.Instrumentation.ActivityMonitor;
import android.test.ActivityInstrumentationTestCase2;
import android.widget.Button;

public class MainActivityTest extends ActivityInstrumentationTestCase2<MainActivity> {

	private MainActivity mActivity;
	private Button run_button = null;
	public static final int INITIAL_POSITION = 0;

	public MainActivityTest() 
	{
		super(MainActivity.class);
	}
	
  protected void setUp() throws Exception 
  {
	    super.setUp();
	    
	    setActivityInitialTouchMode(false);
	    
	    //start activity
	    mActivity = getActivity();
	    //get needed button
	    run_button = (Button) mActivity.findViewById(R.id.button_runOptions);
  }

  public void testMainUI() 
  {
  
	  // register next activity that need to be monitored.
	  ActivityMonitor activityMonitor = getInstrumentation().addMonitor(RunOptions.class.getName(), null, false);
	  
	  mActivity.runOnUiThread(new Runnable() 
	  {
	    @Override
	    public void run() 
	    {
	      // click button and open next activity.
	      run_button.performClick();
	    }
	  });

	  Activity runOptions = getInstrumentation().waitForMonitorWithTimeout(activityMonitor, 5000);
	  // next activity is opened and captured.
	  assertNotNull(runOptions);
	  runOptions.finish();
	  	  	  
  }

}