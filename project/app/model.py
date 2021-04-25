import datetime
from pathlib import Path

import joblib
import pandas as pd
from preprocessing import getData
from fbprophet import Prophet


BASE_DIR = Path(__file__).resolve(strict=True).parent
NOW = datetime.datetime.now()


def train(df=None, parameter = 'Temp-81'):
    model = Prophet()
    model.fit(df)

    joblib.dump(model, Path(BASE_DIR).joinpath(f"joblibs/{parameter}.joblib"))


def predict(df = None, parameter="Temp-81", mins = 180, retrain = None):
    if retrain:
        train(df, parameter)
    
    model_file = Path(BASE_DIR).joinpath(f"joblibs/{parameter}.joblib")
    if not model_file.exists():
        return False

    model = joblib.load(model_file)

    df_forecast = model.make_future_dataframe(periods = int(mins), freq='T', include_history = True)
    forecast = model.predict(df_forecast)

    model.plot(forecast).savefig(f"plots/{parameter}_plot.png")
    model.plot_components(forecast).savefig(f"plots/{parameter}_plot_components.png")

    return forecast.to_dict("records")

def convert(prediction_list):
    output = {}
    for data in prediction_list:
        date = data["ds"]
        output[date] = data["yhat"]
    return output
