# bring in query strings

import pickle
from flask import Flask, request
import pandas as pd

app = Flask(__name__)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return 'Use the /predict endpoint'

@app.route('/predict')
def predict():
    query = request.args
    print(query)
    new = pd.DataFrame({'temperature': [20]})
    prediction = model.predict(new)[0]
    return {'prediction': prediction}

if __name__ == '__main__':
    app.run(port=5000, debug=True)
