# fix the return type

import pickle
from flask import Flask
import pandas as pd

app = Flask(__name__)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    new = pd.DataFrame({'temperature': [20]})
    prediction = model.predict(new)[0]
    # return str(prediction)
    return {'prediction': prediction}

if __name__ == '__main__':
    app.run(port=5000, debug=True)
