import uvicorn

from fastapi import FastAPI, HTTPException, Request, Depends, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from model_weather import convert, predict
from model_bitcoin import predict_bitcoin_value
from database import connect, query, getCurrentValue, writeToDatabase
from preprocessing import getData, df_cutoff
import pandas as pd

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/dynamic", StaticFiles(directory="dynamic"), name="dynamic")

templates = Jinja2Templates(directory="templates")


# pydantic models

class parameterIn(BaseModel):
    sensorId: str
    showPeriod: int
    forecastTime: int


class forecastOut(BaseModel):
    sensorId: str
    forecastOut: dict


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request
    })


@app.get("/forecast_weather")
def forecast_weather(request: Request):
    return templates.TemplateResponse("forecast_weather.html", {
        "request": request
    })


@app.get("/forecast")
async def get_prediction(sensorId='Temp-81', trainTime=3, forecastTime=3):
    '''
	Forecasting the sensor value
	'''
    # Get df data
    df = getData(sensorId)

    # Get data 3 days from last timestamp
    df = df_cutoff(df, trainTime)

    # Update table
    parameters = ['EC-161', 'PH-181', 'Temp-81', 'Light-121', 'Co2-121', 'Temp-121', 'Hum-121']

    last_value_dict = {}

    for params in parameters:
        last_value_dict[params] = getCurrentValue(params)

    # Prediction
    prediction_list = predict(df, sensorId, trainTime, True)

    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model not found.")

    forecastOut = convert(prediction_list)

    writeToDatabase(forecastOut, sensorId)

    response_object = {"parameter": sensorId, "data_dict": df.to_dict(), "table_dict": last_value_dict,
                       "forecastOut": forecastOut}

    return response_object


@app.get("/forecast_bitcoin")
def forecast_bitcoin(request: Request):
    return templates.TemplateResponse("forecast_bitcoin.html", {
        "request": request
    })


@app.get("/predict_bitcoin")
def predict_bitcoin():
    real_predict_price = predict_bitcoin_value()

    print(real_predict_price, type(real_predict_price))

    predict_price = {"predict_price": real_predict_price}

    response_object = {"real_predict_price": predict_price}

    return response_object


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
