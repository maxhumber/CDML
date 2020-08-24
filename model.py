import pickle
import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from utils import DateEncoder, nn

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.keras.models import load_model
from sklearn.feature_selection import SelectKBest

df = pd.read_csv("data/weather_power.csv", parse_dates=[0])

target = 'energy_demand'
y = df[target]
X = df[['date', 'temperature']]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, shuffle=False, random_state=42)

mapper = DataFrameMapper([
    ('date', DateEncoder(), {'input_df': True}),
    (['temperature'], [SimpleImputer(), PolynomialFeatures(degree=2, include_bias=False)]),
], df_out=True)

select = SelectKBest(k=5)
model = KerasRegressor(nn, epochs=100, verbose=0)
pipe = make_pipeline(mapper, select, model)
pipe.fit(X_train, y_train)

pipe.named_steps['kerasregressor'].model.save('model.h5')
pipe.named_steps['kerasregressor'].model = None

with open("pipe.pkl", 'wb') as f:
    pickle.dump(pipe, f)
