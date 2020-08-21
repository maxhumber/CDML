
import os
import pickle

from fastapi import FastAPI
import uvicorn
from typing import Dict
from pydantic import BaseModel

import pandas as pd
from tensorflow.keras.models import load_model
from utils import DateEncoder, nn

app = FastAPI()

with open('pipe.pkl', 'rb') as f:
    pipe = pickle.load(f)

pipe.named_steps['kerasregressor'].model = load_model('model.h5')

class RequestData(BaseModel):
    date: str
    temperature: float

@app.post('/')
async def index(request: RequestData): # add async and RequestData
    new = pd.DataFrame({
        'date': [pd.Timestamp(request.date)],
        'temperature': [request.temperature]
    })
    prediction = float(pipe.predict(new))
    return {'prediction': prediction}

if __name__ == '__main__':
    uvicorn.run(app)
