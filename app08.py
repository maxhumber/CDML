# post request

import uvicorn
from fastapi import FastAPI
import pandas as pd
import pickle
from typing import Dict

from utils import DateEncoder

app = FastAPI()

with open('pipe.pkl', 'rb') as f:
    pipe = pickle.load(f)

@app.post('/')
def index(json_data: Dict):
    new = pd.DataFrame({
        'date': [pd.Timestamp(json_data.get('date'))],
        'temperature': [float(json_data.get('temperature'))]
    })
    prediction = pipe.predict(new)[0]
    return {'mw_prediction': prediction}

if __name__ == '__main__':
    uvicorn.run(app)

# run at command line with:
# uvicorn app:app --port 5000 --reload
