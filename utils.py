import pandas as pd
from sklearn.base import TransformerMixin

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense

class DateEncoder(TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return pd.concat([X.dt.month, X.dt.weekday, X.dt.hour], axis=1)

def nn():
    columns = 5
    model = Sequential()
    model.add(Input(shape=(columns,)))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1))
    model.compile(
        loss='mean_squared_error',
        optimizer='adam',
        metrics=[tf.keras.metrics.RootMeanSquaredError()]
    )
    return model
