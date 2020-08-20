import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn_pandas import DataFrameMapper
from sklearn.pipeline import make_pipeline
import pickle

# stitch
power = pd.read_csv('data/power.csv', parse_dates=[0])
weather = pd.read_csv('data/weather.csv', parse_dates=[0])
df = pd.merge(power, weather, how='left', on='date')
df['temperature'] = df['temperature'].ffill()

# quick EDA
plt.scatter(df['ontario_demand_mw'], df['toronto_demand_mw'], alpha=1/20)
plt.scatter(df['temperature'], df['toronto_demand_mw'], alpha=1/20)
plt.plot(df['date'], df['toronto_demand_mw'])
plt.plot(df['date'], df['temperature'])

df['month'] = df.date.dt.month
df['day'] = df.date.dt.dayofweek
df['hour'] = df.date.dt.hour

# select
y = df['toronto_demand_mw']
X = df[['month', 'day', 'hour', 'temperature']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

# dummy
dummy = DummyRegressor()
dummy.fit(X_train, y_train)
np.sqrt(mean_squared_error(y_test, dummy.predict(X_test)))

# benchmark
benchmark = LinearRegression()
benchmark.fit(X_train, y_train)
benchmark.score(X_train, y_train), benchmark.score(X_test, y_test)
np.sqrt(mean_squared_error(y_test, benchmark.predict(X_test)))

plt.figure(figsize=(10, 5))
plt.plot(range(len(y_test)), y_test)
plt.plot(range(len(y_test)), benchmark.predict(X_test))

# with some feature engineering
mapper = DataFrameMapper([
    ('month', None),
    ('day', None),
    ('hour', None),
    (['temperature'], PolynomialFeatures(degree=2))
], df_out=True)

model = LinearRegression()
pipe = make_pipeline(mapper, model)
pipe.fit(X_train, y_train)
pipe.score(X_test, y_test)

plt.plot(range(len(y_test)), y_test)
plt.plot(range(len(y_test)), pipe.predict(X_test))
np.sqrt(mean_squared_error(y_test, pipe.predict(X_test)))

plt.hist(df['toronto_demand_mw']);

X.sample(1).to_dict(orient='list')
today = pd.DataFrame({'month': [8], 'day': [19], 'hour': [16], 'temperature': [21]})
pipe.predict(today)[0]

with open('pipe.pkl', 'wb') as f:
    pickle.dump(pipe, f)
