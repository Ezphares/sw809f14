package com.gpstracking.app;

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
import java.util.List;
import java.util.Queue;

/**
 * Created by Henrik on 10-04-14.
 */
public class AccelerometerTracker extends Service implements SensorEventListener {
    private final Context mContext;

    protected float x, y, z;
    private Queue acclData;
    private SensorManager mSensorManager;
    private Sensor mSensor;

    public AccelerometerTracker(Context context) {
        this.mContext = context;
        mSensorManager = (SensorManager) context.getSystemService(context.SENSOR_SERVICE);
        acclData = new LinkedList();
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

    boolean peek = false;
    int peeks = 0;

    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        x = sensorEvent.values[0];
        y = sensorEvent.values[1];
        z = sensorEvent.values[2];
        float mAccelCurrent = FloatMath.sqrt(x * x + y * y + z * z);

        peek = false;
        while(acclData.size() >= 50) {
            acclData.remove();
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

        Log.d("Sensor","Avg:" + Float.toString(avg) + " Current: " + Float.toString(mAccelCurrent));
/*
        if(Float.parseFloat(acclData.peek().toString()) > mAccelCurrent)
        {
            final Iterator itr1 = acclData.iterator();
            while(itr1.hasNext())
            {
                float b = Float.parseFloat(itr1.next().toString());
                if(b > avg+treshhold){
                    if(Float.parseFloat(acclData.peek().toString()) > b)
                        peek = true;
                    else
                        peek = false;
                }
                else
                    continue;
            }
        }
        if(peek)
            peeks++;*/


        //Log.d("Sensor", Integer.toString(peeks));
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
