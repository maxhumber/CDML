from fbprophet import Prophet
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn_pandas import DataFrameMapper

power = pd.read_csv('data/power.csv', parse_dates=[0])
weather = pd.read_csv('data/weather.csv', parse_dates=[0])
df = pd.merge(power, weather, how='left', on='date')
df['temperature'] = df['temperature'].ffill()
df = df.rename(columns={'date': 'ds', 'toronto_demand_mw': 'y'})
df = df[['ds', 'y', 'temperature']]
df['temperature^2'] = df['temperature'] ** 2

df_train, df_test = train_test_split(df, test_size=0.1, shuffle=False)

model = Prophet()
model.add_regressor('temperature')
model.add_regressor('temperature^2')
model.fit(df_train)

forecast = model.predict(df)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

model.plot(forecast);
model.plot_components(forecast);
