package com.egyed.adam.guardianangel;

import android.Manifest;
import android.animation.ArgbEvaluator;
import android.animation.ValueAnimator;
import android.content.ComponentName;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.pm.PackageManager;
import android.content.res.Resources;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.ShapeDrawable;
import android.os.IBinder;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v4.content.res.ResourcesCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.text.TextUtils;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.ScaleAnimation;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.ArrayList;
import java.util.StringTokenizer;

public class MainActivity extends AppCompatActivity {




    // Resource caches
    private int mColorHearing;
    private int mColorNotHearing;

    private StringBuilder sb = new StringBuilder();

    private View circle;
    private View innerCircle;
    private View logo;

    private String bgColor = "#969696";

    // View references
    private TextView mStatus;
    private TextView mText;

    private SpeechService mSpeechService;

    private VoiceRecorder mVoiceRecorder;
    private final VoiceRecorder.Callback mVoiceCallback = new VoiceRecorder.Callback() {

        @Override
        public void onVoiceStart() {
            showStatus(true);
            if (mSpeechService != null) {
                mSpeechService.startRecognizing(mVoiceRecorder.getSampleRate());
            }
        }

        @Override
        public void onVoice(byte[] data, int size) {
            if (mSpeechService != null) {
                mSpeechService.recognize(data, size);
            }
        }

        @Override
        public void onVoiceEnd() {
            showStatus(false);
            if (mSpeechService != null) {
                mSpeechService.finishRecognizing();
            }
        }

    };

    private final SpeechService.Listener mSpeechServiceListener =
            new SpeechService.Listener() {
                @Override
                public void onSpeechRecognized(final String text, final boolean isFinal) {
                    if (isFinal) {
                        mVoiceRecorder.dismiss();
                    }
                    if (mText != null && !TextUtils.isEmpty(text)) {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                if (isFinal) {



                                    mText.setText(text + "\n\n" +mText.getText());

                                    sb.append(text).append(" ");

                                    StringTokenizer st = new StringTokenizer(sb.toString());

                                    if (st.countTokens() >= 14) {
                                        ArrayList<String> words = new ArrayList<>(32);

                                        while (st.hasMoreTokens()) {
                                            words.add(st.nextToken());
                                        }

                                        checkSafety(words);

                                        sb.setLength(0);
                                    }

                                } else {
                                    //mText.append(text);
                                }
                            }
                        });
                    }
                }
            };




    @Override
    protected void onStart() {
        super.onStart();

        // Prepare Cloud Speech API
        bindService(new Intent(this, SpeechService.class), mServiceConnection, BIND_AUTO_CREATE);

        // Start listening to voices
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                == PackageManager.PERMISSION_GRANTED) {
            startVoiceRecorder();
        } else if (ActivityCompat.shouldShowRequestPermissionRationale(this,
                Manifest.permission.RECORD_AUDIO)) {
            //showPermissionMessageDialog();
        } else {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.RECORD_AUDIO},
                    1);
        }
    }

    @Override
    protected void onStop() {
        // Stop listening to voice
        stopVoiceRecorder();

        // Stop Cloud Speech API
        mSpeechService.removeListener(mSpeechServiceListener);
        unbindService(mServiceConnection);
        mSpeechService = null;

        super.onStop();
    }

    private final ServiceConnection mServiceConnection = new ServiceConnection() {

        @Override
        public void onServiceConnected(ComponentName componentName, IBinder binder) {
            mSpeechService = SpeechService.from(binder);
            mSpeechService.addListener(mSpeechServiceListener);
            mStatus.setVisibility(View.VISIBLE);
        }

        @Override
        public void onServiceDisconnected(ComponentName componentName) {
            mSpeechService = null;
        }

    };


    private void showStatus(final boolean hearingVoice) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                mStatus.setTextColor(hearingVoice ? mColorHearing : mColorNotHearing);

                if (hearingVoice) {
                    scaleView(circle, 1.0f, 1.4f, 750);
                    scaleView(innerCircle, 1.0f, 1.7f, 2250);
                    scaleView(logo, 1.0f, 1.5f, 1200);

                } else {
                    scaleView(circle, 1.4f, 1.0f, 1000);
                    scaleView(innerCircle, 1.7f, 1.0f, 600);
                    scaleView(logo, 1.5f, 1.0f, 700);
                }
            }
        });
    }

    private void startVoiceRecorder() {
        if (mVoiceRecorder != null) {
            mVoiceRecorder.stop();
        }
        mVoiceRecorder = new VoiceRecorder(mVoiceCallback);
        mVoiceRecorder.start();
    }

    private void stopVoiceRecorder() {
        if (mVoiceRecorder != null) {
            mVoiceRecorder.stop();
            mVoiceRecorder = null;
        }
    }



    private String phonenumber = "6366860271";

    private String message = "Test SMS Message";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final Resources resources = getResources();
        final Resources.Theme theme = getTheme();
        mColorHearing = ResourcesCompat.getColor(resources, R.color.colorHearing, theme);
        mColorNotHearing = ResourcesCompat.getColor(resources, R.color.colorNotHearing, theme);

        mStatus = (TextView) findViewById(R.id.status);
        mText = (TextView) findViewById(R.id.text);
        circle = findViewById(R.id.circleView);
        innerCircle = findViewById(R.id.innerCircleView);
        logo = findViewById(R.id.imageView);

        findViewById(R.id.button_sentimenttest).setVisibility(View.GONE);
        findViewById(R.id.smstest).setVisibility(View.GONE);
        findViewById(R.id.button_speechtest).setVisibility(View.GONE);

    }


    public void startSpeechTest(View view) {
        Toast.makeText(getApplicationContext(),"Starting Speech Test...",
                Toast.LENGTH_SHORT).show();
        Intent intent = new Intent(this, SpeechTestActivity.class);
        startActivity(intent);
    }

    public void startSentimentTest(View view) {
        Toast.makeText(getApplicationContext(),"Starting Sentiment Test...",
                Toast.LENGTH_SHORT).show();
    }

    public void startSMSTest(View view) {
        Toast.makeText(getApplicationContext(),"Sending test SMS...",
                Toast.LENGTH_SHORT).show();



        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.SEND_SMS)
                != PackageManager.PERMISSION_GRANTED) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(this,
                    Manifest.permission.SEND_SMS)) {
            } else {
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.SEND_SMS},
                        0);
            }
        }

        SmsManager smsManager = SmsManager.getDefault();
        smsManager.sendTextMessage("+1" + phonenumber, null, message, null, null);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,String permissions[], int[] grantResults) {
        switch (requestCode) {
            case 0: {
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    SmsManager smsManager = SmsManager.getDefault();

                    smsManager.sendTextMessage("+!"+phonenumber, null, message, null, null);

                    Toast.makeText(getApplicationContext(), "SMS sent.",
                            Toast.LENGTH_LONG).show();
                } else {
                    Toast.makeText(getApplicationContext(),
                            "SMS faild, please try again.", Toast.LENGTH_LONG).show();
                    return;
                }
            }
        }

    }


    private void checkSafety(ArrayList<String> words) {
        // Instantiate the RequestQueue.
        RequestQueue queue = Volley.newRequestQueue(this);

        StringBuilder stringBuilder = new StringBuilder("http://us-central1-guardian-angel-21062019.cloudfunctions.net/predict_threat?text=");


        for (int i = 0; i < words.size(); i++) {

            String word = words.get(i);
            if (word.contains("\'")) continue;
            word = word.replaceAll(".", "+");
            if (word.contains("\\")) continue;
            if (word.contains("/")) continue;
            stringBuilder.append(words).append('+');
        }

        String url =stringBuilder.toString();

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 500 characters of the response string.

                        float score = Float.valueOf(response);

                        String percentDisplay = String.valueOf(response.charAt(2));
                        percentDisplay += response.charAt(3);
                        percentDisplay += "%";

                        ((TextView) findViewById(R.id.percent)).setText(percentDisplay);


                        final GradientDrawable bg = (GradientDrawable) mText.getBackground();

                        int stepCount = 100;
                        final int[] start = new int[]{68, 117, 215};
                        final int[] end = new int[]{215, 67, 67};


                        String resultColor = interp(start, end, (int) (100 * score), stepCount);

                        //bg.setColor(Color.parseColor(resultColor));


                        ValueAnimator colorAnimation = ValueAnimator.ofArgb(Color.parseColor(bgColor), Color.parseColor(resultColor));
                        bgColor = resultColor;
                        colorAnimation.setDuration(1000); // milliseconds
                        colorAnimation.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {

                            @Override
                            public void onAnimationUpdate(ValueAnimator animator) {
                                bg.setColor((int) animator.getAnimatedValue());
                            }

                        });
                        colorAnimation.start();


                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                ((TextView) findViewById(R.id.functionStatus)).setText(error.toString());
                error.printStackTrace();
            }
        });

        // Add the request to the RequestQueue.

        stringRequest.setRetryPolicy(new DefaultRetryPolicy(
                10000,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

        queue.add(stringRequest);
    }

    private void testInternet() {
        // Instantiate the RequestQueue.
        RequestQueue queue = Volley.newRequestQueue(this);
        String url ="http://us-central1-guardian-angel-21062019.cloudfunctions.net/predict_threat?text=hi";

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 500 characters of the response string.
                         ((TextView) findViewById(R.id.functionStatus)).setText("Response is: "+ response);


                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                ((TextView) findViewById(R.id.functionStatus)).setText(error.toString());
                error.printStackTrace();
            }
        });

        // Add the request to the RequestQueue.
        queue.add(stringRequest);
    }

    public void scaleView(View v, float startScale, float endScale, int duration) {

        ScaleAnimation anim = new ScaleAnimation(startScale, endScale, startScale, endScale,
                Animation.RELATIVE_TO_SELF, 0.5f, Animation.RELATIVE_TO_SELF, 0.5f);

        /*
        Animation anim = new ScaleAnimation(
                1f, 1f, // Start and end values for the X axis scaling
                startScale, endScale, // Start and end values for the Y axis scaling
                Animation.RELATIVE_TO_SELF, 1f, // Pivot point of X scaling
                Animation.RELATIVE_TO_SELF, 1f); // Pivot point of Y scaling

                */
        anim.setFillAfter(true); // Needed to keep the result of the animation
        anim.setDuration(duration);
        v.startAnimation(anim);
    }


    public static String interp(final int[] start, final int[] end, final int step, Integer stepCount) {
        if (stepCount == null) stepCount = 256;

        double r = start[0] + (end[0] - start[0])*step / (double) stepCount;
        double g = start[1] + (end[1] - start[1])*step / (double) stepCount;
        double b = start[2] + (end[2] - start[2])*step / (double) stepCount;

        return rgbToHex((int)r, (int)g, (int)b);
    }


    public static String rgbToHex(final int r, final int g, final int b) {
        return String.format("#%02x%02x%02x", r, g, b);
    }
}
