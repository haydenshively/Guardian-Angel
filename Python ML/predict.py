if __name__ == '__main__':
    from keras import models
    lstm = models.load_model('models/basic_lstm.h5')

    import pickle
    with open('models/Tokenizer.pickle', 'rb') as tokenizer_file:
        tokenizer = pickle.load(tokenizer_file)

    from keras.preprocessing.text import Tokenizer
    from keras.preprocessing.sequence import pad_sequences
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
    text_encoded = tokenizer.texts_to_sequences(text)
    text_padded = pad_sequences(text_encoded, maxlen = 59, padding = 'post')

    result = lstm.predict(text_padded)
    print(result)
