# add DataFrameMapper and Imputer

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle
from sklearn.impute import SimpleImputer
from sklearn_pandas import DataFrameMapper

df = pd.read_csv('data/weather_power.csv')

target = 'toronto_demand_mw'
y = df[target]
X = df[['temperature']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

df.info()

mapper = DataFrameMapper([
    # ('temperature', SimpleImputer()) # will break
    (['temperature'], SimpleImputer()) # easy fix, columns vs series
], df_out=True)

mapper.fit_transform(X_train)
