import pickle
import os
from typing import Dict
import pandas as pd
from fastapi import FastAPI
import uvicorn
from utils import DateEncoder

app = FastAPI()

with open("pipe.pkl", 'rb') as f:
    pipe = pickle.load(f)

@app.post("/")
def index(json_data: Dict):
    new = pd.DataFrame({
        'date': [pd.Timestamp(json_data.get('date'))],
        'temperature': [float(json_data.get('temperature'))]
    })
    prediction = pipe.predict(new)[0]
    return {'prediction': prediction}

if __name__ == "__main__":
    uvicorn.run(app)
