from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
from challenge.model import DelayModel

class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int

class Flights(BaseModel):
    flights: List[Flight]

app = FastAPI()

delay_model = DelayModel()

@app.get("/", status_code=200)
async def get_index() -> dict:
    return {
        "status": "Hello World"
    }


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(flights : Flights) -> dict:
    response = {}
    data = pd.read_csv(filepath_or_buffer="/code/data/data.csv")
    airlines = data['OPERA'].unique()
    type_of_flights = data['TIPOVUELO'].unique()
    flights = flights.dict()['flights']
    for flight in flights:
        if flight["MES"] < 1 or flight['MES'] > 12:
            raise HTTPException(status_code=400, detail="Invalid parameter")
        if flight['TIPOVUELO'] not in type_of_flights:
            raise HTTPException(status_code=400, detail="Invalid parameter")   
        if flight['OPERA'] not in airlines:
            raise HTTPException(status_code=400, detail="Invalid parameter")

    flights_data = pd.json_normalize(flights)
    preprocess_data = delay_model.preprocess(data=flights_data)
    predictions = delay_model.predict(preprocess_data)

    response['predict'] = predictions

    return response