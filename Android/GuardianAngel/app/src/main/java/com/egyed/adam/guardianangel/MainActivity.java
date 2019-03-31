package com.egyed.adam.guardianangel;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
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
}
