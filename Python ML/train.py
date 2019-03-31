if __name__ == '__main__':
    import numpy as np
    import json
    import lstm

    dir_in = '_E_Vectors/'
    sequences = np.load(dir_in + 'X.npy')
    sentiment = np.load(dir_in + 'Y.npy')
    embedding_matrix = np.load(dir_in + 'EmbeddingMatrix.npy')

    with open(dir_in + 'Params.json') as param_file:
        params = json.load(param_file)
        vocab_size = params['Vocab Size']
        vector_dims = params['Vector Dims']
        sequence_length = params['Sequence Length']

    basic_lstm = lstm.Basic(vector_dims, embedding_matrix, sequence_length, vocab_size)

    trainer = lstm.Trainer()
    trainer.input = sequences
    trainer.output = sentiment
    trainer.train(basic_lstm.model)

    basic_lstm.save_to_file('models/basic_lstm.h5')
