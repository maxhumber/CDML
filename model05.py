# can pickle, but it would be both?

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle
from sklearn.impute import SimpleImputer
from sklearn_pandas import DataFrameMapper

df = pd.read_csv('data/weather_power.csv')

target = 'energy_demand'
y = df[target]
X = df[['temperature']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

mapper = DataFrameMapper([
    (['temperature'], SimpleImputer())
], df_out=True)

Z_train = mapper.fit_transform(X_train)
Z_test = mapper.transform(X_test)

model = LinearRegression()
model.fit(Z_train, y_train)
round(mean_squared_error(y_test, model.predict(Z_test)) ** (1/2))

# try and predict

X_train.sample(1).to_dict(orient='list')
new = pd.DataFrame({'temperature': [21]})

Z_new = mapper.transform(new)
model.predict(Z_new)[0]

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

model.predict(Z_new)[0]
