import tensorflow as tf
from law.model.base_model import Model
import sklearn.model_selection
import pandas as pd
import numpy as np

class Example(Model):
    def __init__(self, dict_len, n_class, trainable=True, path="./.cache/dl" ):
        super().__init__()

        self.trainable = trainable
        self.path = path + "_" + str(dict_len) + "_" + str(n_class)
        self.model = tf.keras.Sequential()
        self.dict_len = dict_len
        self.n_class = n_class

        self.model.add(tf.keras.layers.Embedding(dict_len, 16))  # 4896是字典的大小
        self.model.add(tf.keras.layers.GlobalAveragePooling1D())
        self.model.add(tf.keras.layers.Dense(16, activation='relu'))
        self.model.add(tf.keras.layers.Dense(self.n_class, activation='sigmoid'))

        self.model.compile(optimizer='adam',
                           loss='sparse_categorical_crossentropy',
                           metrics=['acc'])
        if not trainable:
            self.load()

    def fit(self, X, y):
        if self.trainable:
            # 划分 val 和 test
            X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2, random_state=1)
            X_train, X_val, y_train, y_val = sklearn.model_selection.train_test_split(X_train, y_train, test_size=0.2, random_state=2)

            history = self.model.fit(X_train, y_train,
                                     epochs=300, batch_size=64,
                                     validation_data=(X_val, y_val))
            return history
        else:
            raise KeyError("You cannot train a untrainable model.")

    def evaluate(self, X_test, y_test):
        return self.model.evaluate(X_test, y_test)

    def store(self):
        self.model.save_weights(self.path)

    def load(self):
        self.model.load_weights(self.path)

    def predict(self, mapped_num_list):
        prob = self.model.predict(mapped_num_list)[0]
        return np.argmax(prob)
