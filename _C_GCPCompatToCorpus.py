"""https://cloud.google.com/speech-to-text/docs/sync-recognize#speech-sync-recognize-python"""

def transcribe_short(speech_file, sample_rate):
    import io
    # import google cloud client library
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    # instantiate client
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as speech_handle:
        content = speech_handle.read()

    audio = types.RecognitionAudio(content = content)
    config = types.RecognitionConfig(
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = sample_rate,
        language_code = 'en-US'
    )
    response = client.recognize(config, audio)

    return response.results
    """for result in response.results:
        for alt in result.alternatives:
            print('Transcript: {}'.format(alt.transcript))
            print('Confidence: {}'.format(alt.confidence))"""


if __name__ == '__main__':
    import os

    dir_in = '_C_100ishGCPCompat/'
    dir_out = '_D_1Corpus/'

    files = os.listdir(dir_in)
    files.sort()
    file_count = len(files)

    with open(dir_out + '2.txt', 'wb') as corpus:
        for i in range(file_count):
            filename = files[i]
            if 'meta' in filename: continue

            filename_no_ext = ''.join(filename.split('.')[:-1])
            filename_meta = filename_no_ext + '.meta.txt'

            f = open(dir_in + filename_meta, 'r')
            sample_rate = eval(f.readline())
            f.close()

            results = transcribe_short(dir_in + filename, sample_rate)
            for result in results:
                print(result.alternatives[0].transcript)
                corpus.write((result.alternatives[0].transcript + '\n').encode())
