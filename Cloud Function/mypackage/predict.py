from keras import models
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pickle

lstm = models.load_model('mypackage/lstm.h5')
with open('mypackage/tokenizer.pickle', 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

def batch(string_list):
    global lstm, tokenizer
    text_encoded = tokenizer.texts_to_sequences(string_list)
    text_padded = pad_sequences(text_encoded, maxlen = 59, padding = 'post')
    return lstm.predict(text_padded)

def single(string):
    global lstm, tokenizer
    text_encoded = tokenizer.texts_to_sequences([string])
    text_padded = pad_sequences(text_encoded, maxlen = 59, padding = 'post')
    return lstm.predict(text_padded)[0][0]

if __name__ == '__main__':
    text = [
    """
    all of that but right now you're going to get kicked out and not come back on our premises
    mechanical Camp if she's always video camera me last time her she came in with the
    other gentleman that was doing the same thing. Video camera and she's taking picture
    """,
    """
    conclusion to this question is no show me the word pretext I quoted them saying that the
    program had you can keep screaming on and it doesn't change the point we do not want sympathy
    we do not want pity we want opportunities it's appalling Sunday to me to the mostly religious
    """,
    ]

    result = batch(text)
    print(result)
