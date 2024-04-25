import fastapi
from pydantic import BaseModel
from typing import List
import pandas as pd
from challenge.model import DelayModel

class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int

app = fastapi.FastAPI()

delay_model = DelayModel()


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(flights : List[Flight]) -> dict:
    response = {}
    flights_data = pd.json_normalize(flights)
    predictions = delay_model.predict(flights_data)
    response['predict'] = predictions

    # for flight in flights:
    #     response[flight] = 0
    return response