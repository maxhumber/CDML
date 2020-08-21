import pandas as pd
from sklearn.base import TransformerMixin

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input

class DateEncoder(TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return pd.concat([X.dt.month, X.dt.weekday, X.dt.hour], axis=1)

def nn():
    columns = 5
    m = Sequential()
    m.add(Input(shape=(columns,)))
    m.add(Dense(10, activation='relu'))
    m.add(Dense(10, activation='relu'))
    m.add(Dense(1))
    m.compile(
        loss='mean_squared_error',
        optimizer='adam',
        metrics=[tf.keras.metrics.RootMeanSquaredError()]
    )
    return m
