# Guardian-Angel
LSTM for sentiment analysis and detection of domestic violence | LA Hacks 2019

This is a quick project that my roommates and I did for LA Hacks 2019. We wanted to use
a smartphone's microphone to detect arguments and domestic violence. Lacking a dataset,
we downloaded videos of Walmart fights from YouTube and trained and LSTM for sentiment
analysis.

[Adam Egyed](https://github.com/adamegyed) built an Android app that connects to a GCP
Cloud Function that runs the ML. Data analysis and model training was done by me
in Python.

## Results

Sadly, the results weren't great. The LSTM only occassionally identified violent phrases
successfully. We believe this is because the transcripts of the Walmart videos were too
low quality -- arguments are difficult to convert into organized sentences. In any case,
the potential for false positives is far too high for this app to be practical. Further
development would require a better dataset.
