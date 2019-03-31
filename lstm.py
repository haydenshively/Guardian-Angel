"""https://doi.org/10.1016/j.procs.2015.02.112"""
"""https://arxiv.org/pdf/1811.08065.pdf"""
"""https://www.liip.ch/en/blog/sentiment-detection-with-keras-word-embeddings-and-lstm-deep-learning-networks"""

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

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

    def __init__(self, embedded_vect_dims, learning_style = default_learning_style):
        self.embedded_vect_dims = embedded_vect_dims

        self.model = Basic._architecture(self.embedded_vect_dims)
        self.learning_style = learning_style

    @staticmethod
    def _architecture(embedded_vect_dims):
        archit = Sequential()

        archit.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
        archit.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        archit.add(MaxPooling2D(pool_size=(2, 2)))
        archit.add(Dropout(0.25))
        archit.add(Flatten())
        archit.add(Dense(128, activation='relu'))
        archit.add(Dropout(0.5))
        archit.add(Dense(1, activation='sigmoid'))

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

        self.data_generator = None
        self.test_percent = 10

    def train(self, model, epochs = 12, batch_size = 128):
        test_index = self.input.shape[0]*(100 - self.test_percent)//100

        x_train = self.input[:test_index]
        y_train = self.output[:test_index]
        x_test = self.input[test_index:]
        y_test = self.output[test_index:]

        if self.data_generator is None:
            model.fit(x_train, y_train,
                      batch_size = batch_size,
                      epochs = epochs,
                      verbose = 1,
                      validation_data = (x_test, y_test))

        else:
            model.fit_generator(self.data_generator.flow(x_train, y_train, batch_size = batch_size),
                                steps_per_epoch = x_train.shape[0]//batch_size,
                                epochs = epochs,
                                verbose = 1,
                                validation_data = (x_test, y_test))


    @staticmethod
    def normalize_input(input):
        return input.astype('float32')/input.max()

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, new_input):
        if type(new_input) is np.ndarray:
            self._input = Trainer.normalize_input(new_input)
        else: self._input = new_input

    @staticmethod
    def normalize_output(output):
        if len(output.shape) is 1: return keras.utils.to_categorical(output)
        else: return output

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, new_output):
        if type(new_output) is np.ndarray:
            self._output = Trainer.normalize_output(new_output)
        else: self._output = new_output
