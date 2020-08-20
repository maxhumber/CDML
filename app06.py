# connect model06

import pickle
from flask import Flask, request
import pandas as pd

app = Flask(__name__)

with open('pipe.pkl', 'rb') as f:
    pipe = pickle.load(f)

@app.route('/')
def index():
    return 'Use the /predict endpoint with a temperature argument'

@app.route('/predict')
def predict():
    query = request.args
    temperature = float(query.get('temperature'))
    new = pd.DataFrame({'temperature': [temperature]})
    prediction = pipe.predict(new)[0]
    return {'prediction': prediction}

if __name__ == '__main__':
    app.run(port=5000, debug=True)
