# !pip install fastapi uvicorn

import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {'hello': 'world'}

@app.get('/predict')
def predict(date: str, temperature: float):
    return {'date': date, 'temperature': temperature}


if __name__ == '__main__':
    uvicorn.run(app)

# run at command line with:
# uvicorn app:app --port 5000
