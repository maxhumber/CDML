# add pipeline

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle
from sklearn.impute import SimpleImputer
from sklearn_pandas import DataFrameMapper
from sklearn.pipeline import make_pipeline

df = pd.read_csv('data/weather_power.csv')

target = 'energy_demand'
y = df[target]
X = df[['temperature']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

mapper = DataFrameMapper([
    (['temperature'], SimpleImputer())
], df_out=True)

model = LinearRegression()

pipe = make_pipeline(mapper, model)
pipe.fit(X_train, y_train)
round(mean_squared_error(y_test, pipe.predict(X_test)) ** (1/2))

# try and predict

new = pd.DataFrame({'temperature': [21]})
pipe.predict(new)[0]

with open('pipe.pkl', 'wb') as f:
    pickle.dump(pipe, f)

with open('pipe.pkl', 'rb') as f:
    pipe = pickle.load(f)

pipe.predict(new)[0]
