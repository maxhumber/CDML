# eda for dates and shit

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle
from sklearn.impute import SimpleImputer
from sklearn_pandas import DataFrameMapper
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.base import TransformerMixin

from matplotlib import pyplot as plt

df = pd.read_csv('data/weather_power.csv', parse_dates=[0])

target = 'energy_demand'
y = df[target]
X = df[['date', 'temperature']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

class DateEncoder(TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return pd.concat([X.dt.month, X.dt.weekday, X.dt.hour], axis=1)

mapper = DataFrameMapper([
    ('date', DateEncoder(), {'input_df': True}),
    (['temperature'], [SimpleImputer(), PolynomialFeatures(degree=2, include_bias=False)])
], df_out=True)

model = LinearRegression()
pipe = make_pipeline(mapper, model)
pipe.fit(X_train, y_train)
pipe.score(X_test, y_test)

plt.plot(range(len(y_test)), y_test)
plt.plot(range(len(y_test)), pipe.predict(X_test))
mean_squared_error(y_test, pipe.predict(X_test)) ** (1/2)

with open('pipe.pkl', 'wb') as f:
    pickle.dump(pipe, f)
