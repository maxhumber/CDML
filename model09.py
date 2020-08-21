# try keras

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle
from sklearn.impute import SimpleImputer
from sklearn_pandas import DataFrameMapper
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input

from utils import DateEncoder

df = pd.read_csv('data/weather_power.csv', parse_dates=[0])

target = 'energy_demand'
y = df[target]
X = df[['date', 'temperature']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

mapper = DataFrameMapper([
    ('date', DateEncoder(), {'input_df': True}),
    (['temperature'], [SimpleImputer(), PolynomialFeatures(degree=2, include_bias=False)])
], df_out=True)

Z_train = mapper.fit_transform(X_train)
Z_test = mapper.transform(X_test)

model = Sequential()
model.add(Input(shape=(Z_train.shape[1],)))
model.add(Dense(10, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(1))

model.compile(
    loss='mean_squared_error',
    optimizer='adam',
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

model.fit(
    Z_train, y_train,
    epochs=100, batch_size=32,
    validation_data=(Z_test, y_test)
)

new = pd.DataFrame({
    'date': [pd.Timestamp('now')],
    'temperature': [17]
})

model.predict(mapper.transform(new))[0][0]

from matplotlib import pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(X_train['date'], y_train, alpha=1/2);
plt.plot(X_train['date'], model.predict(Z_train).flatten(), alpha=1/2);

plt.figure(figsize=(10, 5))
plt.plot(X_test['date'], y_test, alpha=1/2);
plt.plot(X_test['date'], model.predict(Z_test).flatten(), alpha=1/2);

round(mean_squared_error(y_test, model.predict(Z_test)) ** (1/2))

model.evaluate(Z_test, y_test)
r2_score(y_test, model.predict(Z_test)), r2_score(y_test, model.predict(Z_test))


#
