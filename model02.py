# try with linear regression

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle

df = pd.read_csv('data/weather_power.csv')

target = 'toronto_demand_mw'
y = df[target]
X = df[['temperature']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

model = LinearRegression()
model.fit(X_train, y_train)
round(mean_squared_error(y_test, model.predict(X_test)) ** (1/2))

# will break
