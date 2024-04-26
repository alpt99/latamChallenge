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


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(flights : Flights) -> dict:
    response = {}
    # flights_data = pd.json_normalize(flights)
    # predictions = delay_model.predict(flights_data)
    # response['predict'] = predictions

    # # for flight in flights:
    data = pd.read_csv(filepath_or_buffer="/code/data/data.csv")
    airlines = data['OPERA'].unique()
    type_of_flights = data['TIPOVUELO'].unique()
    # #     response[flight] = 0
        # Log the incoming data
    print("Incoming flights data:", flights)
    # if len(flights) == 0:
    #     raise HTTPException(status_code=400, detail="No data provided")
    flights = flights.dict()['flights']
    for flight in flights:
        if flight["MES"] < 1 or flight['MES'] > 12:
            raise HTTPException(status_code=400, detail="Invalid parameter")
        if flight['TIPOVUELO'] not in type_of_flights:
            raise HTTPException(status_code=400, detail="Invalid parameter")   
        if flight['OPERA'] not in airlines:
            raise HTTPException(status_code=400, detail="Invalid parameter")

    # Normalize the data
    flights_data = pd.json_normalize(flights)

    # Log the normalized data
    print("Normalized flights data:", flights_data)

    # Predict using the delay model
    predictions = delay_model.predict(flights_data)

    # Log the predictions
    print("Predictions:", predictions)

    response['predict'] = predictions

    return response