import pickle
import pandas as pd

from fastapi import FastAPI
import uvicorn

app = FastAPI()

with open("pipe.pkl", 'rb') as f:
    pipe = pickle.load(f)

@app.get("/")
def index():
    return 'Use the /predict endpoint'

@app.get("/predict")
def predict(temperature: float):
    new = pd.DataFrame({'temperature': [temperature]})
    prediction = pipe.predict(new)[0]
    return {'prediction': prediction}

if __name__ == "__main__":
    uvicorn.run(app)
