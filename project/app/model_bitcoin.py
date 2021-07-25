import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import requests
from datetime import datetime
# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Activation

from sklearn.preprocessing import MinMaxScaler

def load_data():
    parameters = {
        "start" : '2021-01-01T00:00:00',
        "stop" : '2021-05-01T00:00:00',
        "granularity" : '86400'
    }           

    response = requests.get("https://api.pro.coinbase.com/products/BTC-USD/candles", params = parameters)
    data = response.json()
    df = pd.DataFrame(data, columns = ['time', 'low', 'high', 'open', 'close', 'volume'])
    return df

def preprocessing_data(df=None):
    # Sort value with most current data and convert to datetime
    df = df.sort_values('time')
    df['time'] = pd.to_datetime(df['time'], unit = 's')

    # First thing is to fix the data for bars/candles where there are no trades. 
    # Volume/trades are a single event so fill na's with zeroes for relevant fields...
    df['volume'].fillna(value=0, inplace=True)

    # next we need to fix the OHLC (open high low close) data which is a continuous timeseries so
    # lets fill forwards those values...
    df['open'].fillna(method='ffill', inplace=True)
    df['high'].fillna(method='ffill', inplace=True)
    df['low'].fillna(method='ffill', inplace=True)
    df['close'].fillna(method='ffill', inplace=True)

    #load the dataset 
    data = df[['time','open']]
    data.index = data['time']
    data = data.drop('time', axis = 1)
    return data

def prepare_train_data(training_set=[]):
    # Data preprocess
    training_set = np.reshape(training_set, (len(training_set), 1))
    X_train = training_set[0:len(training_set)-1]
    y_train = training_set[1:len(training_set)]
    X_train = np.reshape(X_train, (len(X_train), 1, 1))
    return X_train, y_train

def build_model():
    model = Sequential()
    model.add(LSTM(128,activation="sigmoid",input_shape=(1,1)))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def train_model(model, X_train, y_train):
    model.fit(X_train, y_train, epochs=50, batch_size=50, verbose=2)
    return model

def predict_bitcoin_value():
    df = load_data()
    data = preprocessing_data(df)
    training_set = data.values

    # scale the data
    sc = MinMaxScaler()
    training_set = sc.fit_transform(training_set)
    X_train, y_train = prepare_train_data(training_set)
    model = build_model()
    model = train_model(model, X_train, y_train)

    #predict today price
    last_price = data[-1:].values
    last_price = sc.transform(last_price).reshape(1,1,1)

    predict_price = model.predict(last_price)
    real_predict_price = sc.inverse_transform(predict_price)
    real_predict_price.reshape(1)
    real_predict_price = real_predict_price.item(0)
    return real_predict_price















