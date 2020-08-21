# dummy example, get to a model as soon as possible

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
import pickle

df = pd.read_csv('data/weather_power.csv')

target = 'energy_demand'
y = df[target]
X = df[['temperature']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

model = DummyRegressor()
model.fit(X_train, y_train)
round(mean_squared_error(y_test, model.predict(X_test)) ** (1/2))

X.sample(1).to_dict(orient='list')
new = pd.DataFrame({'temperature': [21]})
model.predict(new)[0]

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

model.predict(new)[0]
