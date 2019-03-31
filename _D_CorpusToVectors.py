"""https://nlp.stanford.edu/projects/glove/"""
import numpy as np

def find_mean_sequence_length(corpus_path):
    with open(corpus_path) as corpus:
        sum = 0
        for i, line in enumerate(corpus):
            sum += len(corpus.readline())

        return int(sum/(i + 1))

def create_word_to_vec_dict(glove_path):
    word_to_vec_dict = {}
    with open(glove_path) as glove:
        for entry in glove:
            values = entry.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype = 'float32')
            word_to_vec_dict[word] = coefs

    return word_to_vec_dict

def get_lines_for(filename):
    lines = []
    with open(filename) as file:
        for i, line in enumerate(file):
            lines.append(line)
    return lines


if __name__ == '__main__':

    word_to_vec_dict = create_word_to_vec_dict('glove.twitter.27B.50d.txt')
    vector_dims = 50

    dir_in = '_D_1Corpus/'
    dir_out = '_E_Vectors/'

    filename_positive = '1.txt'
    filename_negative = '2.txt'

    positives = get_lines_for(dir_in + filename_positive)
    negatives = get_lines_for(dir_in + filename_negative)
    samples = positives + negatives

    positive_count = len(positives)
    negative_count = len(negatives)

    positive_labels = np.ones((positive_count))
    negative_labels = np.zeros((negative_count))
    labels = np.hstack((positive_labels, negative_labels))

    from keras.preprocessing.text import Tokenizer
    from keras.preprocessing.sequence import pad_sequences

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(samples)
    vocab_size = len(tokenizer.word_index) + 1

    samples_encoded = tokenizer.texts_to_sequences(samples)
    #print(samples_encoded)
    max_length = find_mean_sequence_length(dir_in + filename_positive) + 10
    samples_padded = pad_sequences(samples_encoded, maxlen = max_length, padding = 'post')
    #print(samples_padded)

    embedding_matrix = np.zeros((vocab_size, vector_dims))
    for word, i in tokenizer.word_index.items():
        embedding_vector = word_to_vec_dict.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    np.save(dir_out + 'X.npy', samples_padded)
    np.save(dir_out + 'Y.npy', labels)
    np.save(dir_out + 'EmbeddingMatrix.npy', embedding_matrix)

    import json
    params = {'Vocab Size' : vocab_size, 'Sequence Length' : max_length, 'Vector Dims' : vector_dims}
    with open(dir_out + 'Params.json', 'w') as param_file:
        json.dump(params, param_file)



    """FIRST CORPUS
    filename = '1.txt'
    sequence_length = find_mean_sequence_length(dir_in + filename) + 10
    sequences_as_vectors = []
    with open(dir_in + filename) as corpus:
        for line in corpus:
            words = line.lower().split()
            sequence = []
            for word in words:
                try:
                    word_as_vect = word_to_vec_dict[word]
                except KeyError:
                    print('Could not find a mapping for ' + word)
                    word_as_vect = np.zeros(vector_dims, dtype = 'float32')
                sequence.append(word_as_vect)
                if len(sequence) == sequence_length: break
            while len(sequence) <= sequence_length:
                sequence.append(np.zeros(vector_dims, dtype = 'float32'))
            sequences_as_vectors.append(np.asarray(sequence))

    sequences_as_vectors = np.moveaxis(np.dstack(sequences_as_vectors), -1, 0)
    print(sequences_as_vectors.shape)
    filename_no_ext = ''.join(filename.split('.')[:-1])
    np.save(dir_out + filename_no_ext + '.npy', sequences_as_vectors)

    SECOND CORPUS
    filename = '2.txt'
    sequences_as_vectors = []
    with open(dir_in + filename) as corpus:
        for line in corpus:
            words = line.lower().split()
            sequence_A = []
            sequence_B = []
            sequence_current = []
            for word in words:
                try:
                    word_as_vect = word_to_vec_dict[word]
                except KeyError:
                    print('Could not find a mapping for ' + word)
                    word_as_vect = np.zeros(vector_dims, dtype = 'float32')
                sequence_current.append(word_as_vect)
                if len(sequence_current) == sequence_length:
                    if len(sequence_A) is 0:
                        sequence_A = sequence_current.copy()
                        sequence_current = []
                    else:
                        sequence_B = sequence_current
                        break
            while len(sequence_A) <= sequence_length:
                sequence_A.append(np.zeros(vector_dims, dtype = 'float32'))
            while len(sequence_B) <= sequence_length:
                sequence_B.append(np.zeros(vector_dims, dtype = 'float32'))
            sequences_as_vectors.append(np.asarray(sequence_A))
            sequences_as_vectors.append(np.asarray(sequence_B))

    sequences_as_vectors = np.moveaxis(np.dstack(sequences_as_vectors), -1, 0)
    print(sequences_as_vectors.shape)
    filename_no_ext = ''.join(filename.split('.')[:-1])
    np.save(dir_out + filename_no_ext + '.npy', sequences_as_vectors)"""
