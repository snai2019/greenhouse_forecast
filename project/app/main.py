from fastapi import FastAPI, HTTPException, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from model import convert, predict
from database import connect, query, getCurrentValue, writeToDatabase
from preprocessing import getData, df_cutoff
from send_sms import sendAlert
import pandas as pd

app = FastAPI()

templates = Jinja2Templates(directory = "templates")

#pydantic models

class parameterIn(BaseModel):
	sensorId: str
	showPeriod: int
	forecastTime: int

class forecastOut(BaseModel):
	sensorId: str
	forecastOut: dict

@app.get("/home")
def home(request: Request):
	'''
	Display the forecasting results
	'''
	# Update table
	parameters = ['EC-161', 'PH-181', 'Temp-81', 'Light-121', 'Co2-121', 'Temp-121', 'Hum-121']
	params_dict = {}

	for params in parameters:
		params_dict[params] = getCurrentValue(params)
	
	return templates.TemplateResponse("home.html", {
		"request": request,
		"params_dict" : params_dict
	})

@app.get("/updateTable")
def table():
	'''
	Update table value
	'''
	parameters = ['EC-161', 'PH-181', 'Temp-81', 'Light-121', 'Co2-121', 'Temp-121', 'Hum-121']
	params_dict = {}

	for params in parameters:
		params_dict[params] = getCurrentValue(params)
	
	return params_dict

@app.post("/forecast")
async def get_prediction(sensorId = 'Temp-81', showPeriod = 3, forecastTime = 3):
	'''
	Forecasting the sensor value
	'''
	# Get df data
	df = getData(sensorId)

	# Get data 3 days from last timestamp
	df = df_cutoff(df, showPeriod)

	# Update table
	parameters = ['EC-161', 'PH-181', 'Temp-81', 'Light-121', 'Co2-121', 'Temp-121', 'Hum-121']
	
	last_value_dict = {}

	for params in parameters:
		last_value_dict[params] = getCurrentValue(params)

	# Prediction
	prediction_list = predict(df, parameter = sensorId, hours = forecastTime, retrain = True)

	if not prediction_list:
		raise HTTPException(status_code=400, detail="Model not found.")

	forecastOut = convert(prediction_list)

	writeToDatabase(forecastOut, sensorId)

	# Alert
	alertDict = {'EC-161': 500, 'PH-181': 50, 'Temp-81':30, 'Light-121':500, 'Co2-121':1000, 'Temp-121':30, 'Hum-121':500}
	for data in forecastOut.values():
		if data > alertDict[sensorId]:
			sendAlert(sensorId)
			break

	response_object = {"parameter": sensorId, "data_dict": df.to_dict(), "table_dict": last_value_dict, "forecastOut": forecastOut}


	return response_object