import tensorflow as tf
from base_model import Model
import sklearn.model_selection
import pandas as pd

class Example(Model):
    def __init__(self):
        super().__init__()

        self.model = tf.keras.Sequential()

        self.model.add(tf.keras.layers.Embedding(4896, 16)) # 4896是字典的大小
        self.model.add(tf.keras.layers.GlobalAveragePooling1D())
        self.model.add(tf.keras.layers.Dense(16, activation='relu'))
        self.model.add(tf.keras.layers.Dense(61, activation='sigmoid'))

        self.model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['acc'])


    def fit(self, X, y):

        # 划分 val 和 test
        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2, random_state=1)
        X_train, X_val, y_train, y_val = sklearn.model_selection.train_test_split(X_train, y_train, test_size=0.2, random_state=2)

        history = self.model.fit(X,y,epochs=300, batch_size=64, validation_data=(X_val, y_val))
        return history

    def evaluate(self, X_test, y_test):
        return self.model.evaluate(X_test, y_test)

    def predict(self, X):
        # TODO
        prob = self.model.predict(x_tt)[0]
        return pd.factorize(law_list.drop(index=drop_list,axis=0)['tiao_used'])[1][np.argmax(prob)]
