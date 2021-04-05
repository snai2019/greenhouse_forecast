import pyodbc
import sqlalchemy as sal
from sqlalchemy import create_engine, insert, text
from sqlalchemy import Table, Column, String, Integer, DateTime, Float, MetaData
import pandas as pd 
import urllib 

server_name = 'MSI\SQLEXPRESS;'
database_name = 'SensorData'

def connect(server_name = server_name, database_name = database_name):
    '''
    Establishing connection with database
    '''
    # provide server name, database name
    # connection_string = urllib.parse.quote_plus(
    #                             "DRIVER={ODBC Driver 17 for SQL Server};"
    #                             "SERVER=DESKTOP-V3FLG05\SQLSERVER;"
    #                             "DATABASE=SensorData;"
    #                             "Trusted_Connection=yes")
                                 
    connection_string = urllib.parse.quote_plus(
                                    "DRIVER={ODBC Driver 17 for SQL Server};"
                                    "SERVER=MSI\SQLEXPRESS;"
                                    "DATABASE=SensorData;"
                                    "Trusted_Connection=yes;")

    engine = sal.create_engine("mssql+pyodbc:///?odbc_connect={}".format(connection_string))

    # establishing the connection to database using engine as an interface
    connect = engine.connect()

    return connect


def query(parameter = 'Temp-81'):
    '''
    Query the sensor data for training model and predict
    '''
    # establish connection
    engine = connect()

    # Extracting table contents
    # reading a SQL query using pandas
    query_command = "SELECT * FROM SensorData.dbo.Sensor_Data_Log WHERE Name = '" + parameter + "';"
    sql_query = pd.read_sql_query(query_command, engine)
    # saving SQL table in a pandas data frame
    df = pd.DataFrame(sql_query)
    # printing the dataframe
    return df

def getCurrentValue(parameter= 'Temp-81'):
    '''
    Get the current value of the sensor parameter from database and show to GUI
    '''
    # establish connection
    engine = connect()

    # reading a SQL query using pandas
    query_command = "SELECT TOP 1 Value FROM SensorData.dbo.Sensor_Data_Log  WHERE Name = '"+ parameter +"' ORDER BY Creation_Time DESC;"
    sql_query = pd.read_sql_query(query_command, engine)
    # saving SQL table in a pandas data frame
    df = pd.DataFrame(sql_query)
    # get the value
    val = round(float(df['Value'][0]), 2)

    return val

def writeToDatabase(forecastOut = {}, sensor = None):
    ''' Write the forecasting data to the database
    '''
    # establish connection
    engine = connect()

    sql = text('DROP TABLE IF EXISTS dbo.forecast;')
    result = engine.execute(sql)

    metadata = MetaData()

    # create table 
    forecast = Table('forecast', 
        metadata, 
        Column('Time',  DateTime), 
        Column('Sensor', String), 
        Column('Value', Float),)

    metadata.create_all(engine)

    for key, value in forecastOut.items():
        inDataQuery = insert(forecast).values(Time = key, Sensor =sensor, Value = value)
        ResultProxy = engine.execute(inDataQuery)

    # insert value to table
