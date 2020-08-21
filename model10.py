# keras save

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
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.keras.models import load_model

from sklearn.feature_selection import SelectKBest # needed as a bridge

from utils import DateEncoder, nn

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

columns = 5
select = SelectKBest(k=columns)

select.fit_transform(Z_train, y_train)

# def nn():
#     columns = 5
#     m = Sequential()
#     m.add(Input(shape=(columns,)))
#     m.add(Dense(10, activation='relu'))
#     m.add(Dense(10, activation='relu'))
#     m.add(Dense(1))
#     m.compile(
#         loss='mean_squared_error',
#         optimizer='adam',
#         metrics=[tf.keras.metrics.RootMeanSquaredError()]
#     )
#     return m

model = KerasRegressor(nn, epochs=100, batch_size=32, verbose=0)

pipe = make_pipeline(mapper, select, model)
pipe.fit(X_train, y_train)

new = pd.DataFrame({
    'date': [pd.Timestamp('now')],
    'temperature': [17]
})

float(pipe.predict(new))

pipe.named_steps['kerasregressor'].model.save('model.h5')
pipe.named_steps['kerasregressor'].model = None

with open('pipe.pkl', 'wb') as f:
    pickle.dump(pipe, f)

with open('pipe.pkl', 'rb') as f:
    pipe = pickle.load(f)

pipe.named_steps['kerasregressor'].model = load_model('model.h5')

float(pipe.predict(new))
