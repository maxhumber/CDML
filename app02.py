# just adding in the model, but it will break

import pickle
from flask import Flask
import pandas as pd

app = Flask(__name__)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    new = pd.DataFrame({'temperature': [20]})
    prediction = model.predict(new)
    print(prediction)
    return prediction

if __name__ == '__main__':
    app.run(port=5000, debug=True)
