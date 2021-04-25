from database import connect, query
import plotly.graph_objs as go
import plotly.offline as py
import pandas as pd
from datetime import datetime, timedelta

server_name = 'DESKTOP-V3FLG05\SQLSERVER'
database_name = 'SensorData'

#Establising connection
connect(server_name, database_name)

current_time = datetime.now()
# Time to get the data
def df_cutoff(df = None, trainTime = 3):
    last_time = df.tail(1).ds
    last_time = pd.to_datetime(last_time)
    
    last_N_days = last_time - timedelta(days = int(trainTime))
    last_N_days = last_N_days.values[0]
    df = df[df['ds']>=last_N_days]
    
    return df


#get data
def getData(parameter = 'Temp-81'):
    df = query(parameter)

    df = df[['Creation_Time','Value']]
    df = df.rename(columns={'Creation_Time': 'ds', 'Value': 'y'})

    df.reset_index(inplace = True, drop = True)
    df['ds'] = pd.to_datetime(df['ds'])

    nonull_series = (df != 0).any(axis=1)
    df = df.loc[nonull_series]
    df.dropna(inplace = True)
    df['y'] = pd.to_numeric(df['y'],errors='ignore')

    # fig = go.Figure(data=go.Scatter(x=df['ds'], y=df['y']))
    # fig.show() 

    wired_sensors = ['Co2-121', 'EC-121']

    if parameter in wired_sensors:
        df = df[0::15]

    return df

