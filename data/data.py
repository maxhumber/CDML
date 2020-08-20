import pandas as pd

power = pd.read_csv('data/power.csv', parse_dates=[0])
weather = pd.read_csv('data/weather.csv', parse_dates=[0])
df = pd.merge(power, weather, how='left', on='date')

df.to_csv('data/weather_power.csv', index=False)
