package dk.aau.student.runapp;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.IBinder;
import android.util.FloatMath;
import android.util.Log;

import java.util.Iterator;
import java.util.LinkedList;
import java.util.Queue;

/**
 * Created by Henrik on 10-04-14.
 */
public class AccelerometerTracker extends Service implements SensorEventListener {
    private final Context mContext;

    protected float x, y, z;
    private Queue acclData;
    private Queue peeks;
    private SensorManager mSensorManager;
    private Sensor mSensor;
    public String state;

    public AccelerometerTracker(Context context) {
        this.mContext = context;
        mSensorManager = (SensorManager) context.getSystemService(context.SENSOR_SERVICE);
        acclData = new LinkedList();
        peeks = new LinkedList();
        getAccelerometer();

    }

    public Boolean getAccelerometer() {
        try {
            Log.d("Sensor", "Loaded");


            if(mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) != null)
            {
                //Sensor
                mSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
                mSensorManager.registerListener(this, mSensor,SensorManager.SENSOR_DELAY_NORMAL);
                Log.d("Sensor", "Started");
            }


        } catch (Exception e) {
            e.printStackTrace();
        }

        return true;
    }


    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        x = sensorEvent.values[0];
        y = sensorEvent.values[1];
        z = sensorEvent.values[2];
        float mAccelCurrent = FloatMath.sqrt(x * x + y * y + z * z);

        if(acclData.size() >= 50) {
            acclData.poll();
        }

        acclData.add(mAccelCurrent);
        float treshhold = 0.5f;

        final Iterator itr = acclData.iterator();
        float avg = 0f;
        while(itr.hasNext()){
            float a = Float.parseFloat(itr.next().toString());
            avg += a;
        }
        avg = avg / acclData.size();

        Log.d("Sensor","Avg:" + Float.toString(avg) + " Current: " + Float.toString(mAccelCurrent) + (mAccelCurrent > avg+treshhold ? " ACTION" : " NO ACTION"));

        if(peeks.size() >= 50) {
            peeks.poll();
        }
        if(mAccelCurrent > avg+treshhold)
            peeks.add(1);
        else
            peeks.add(0);

        final Iterator itr1 = peeks.iterator();
        int temp = 0;
        while(itr1.hasNext()){
            float a = Integer.parseInt(itr1.next().toString());
            temp += a;
        }

        state = temp > 0 ? "Action" : "No Action";

        Log.d("Sensor",Integer.toString(temp));
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
