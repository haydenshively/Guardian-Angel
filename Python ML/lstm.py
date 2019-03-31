"""https://doi.org/10.1016/j.procs.2015.02.112"""
"""https://arxiv.org/pdf/1811.08065.pdf"""
"""https://www.liip.ch/en/blog/sentiment-detection-with-keras-word-embeddings-and-lstm-deep-learning-networks"""
"""https://machinelearningmastery.com/use-word-embedding-layers-deep-learning-keras/"""

import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import LSTM, Embedding

import numpy as np

class LearningStyle(object):
    def __init__(self, loss, optimizer, metrics):
        self.loss = loss
        self.optimizer = optimizer
        self.metrics = metrics

    def apply_to(self, model):
        model.compile(loss = self.loss, optimizer = self.optimizer, metrics = self.metrics)

class Basic(object):
    default_learning_style = LearningStyle(keras.losses.binary_crossentropy, keras.optimizers.Adam(), metrics = ['accuracy'])

    def __init__(self, vector_dims, embedding_matrix, sequence_length, vocab_size, learning_style = default_learning_style):
        self.vector_dims = vector_dims
        self.embedding_matrix = embedding_matrix
        self.sequence_length = sequence_length
        self.vocab_size = vocab_size

        self.model = self._architecture()
        self.learning_style = learning_style

    def _architecture(self):
        archit = Sequential()

        archit.add(Embedding(
            self.vocab_size,
            self.vector_dims,
            weights = [self.embedding_matrix],
            input_length = self.sequence_length,
            trainable = False))
        archit.add(LSTM(50))
        archit.add(Dense(1, activation = 'sigmoid'))

        return archit

    def save_to_file(self, path = 'model.h5'):
        self.model.save(path)

    @property
    def learning_style(self):
        return self._learning_style

    @learning_style.setter
    def learning_style(self, new_learning_style):
        self._learning_style = new_learning_style
        self._learning_style.apply_to(self.model)


class Trainer(object):
    def __init__(self):
        self.input = None
        self.output = None

    def train(self, model, epochs = 50, batch_size = 10):
        print(model.summary())
        model.fit(self.input, self.output, epochs = epochs, batch_size = batch_size, verbose = 1, shuffle = True)
