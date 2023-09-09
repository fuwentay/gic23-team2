from sqlalchemy import create_engine
import pandas as pd
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from datetime import datetime, timedelta

# Connect to PostgreSQL database
# engine = create_engine('postgresql://username:password@localhost:5432/database')

# Load CSV data & Insert into database table
instrument_df = pd.read_csv("./inputs/instruments-cleaned.csv")
market_values_df = pd.read_csv("./inputs/market-values-cleaned.csv")
transactions_df = pd.read_csv("./inputs/transactions-cleaned.csv")

# instrument_df.to_sql('instruments', engine, if_exists='replace', index=False)
# market_values_df.to_sql('marketVals', engine, if_exists='replace', index=False)
# transactions_df.to_sql('transactions', engine, if_exists='replace', index=False)

# Data Preprocessing
# Set 'createdAt' to datetime type
market_values_df["createdAt"] = pd.to_datetime(market_values_df["createdAt"])
market_values_df.set_index("createdAt", inplace=True)


# Predict market values using ARIMA
def arima_forecast(data, instrument_id):
    instrument_data = data[data["instrumentId"] == instrument_id]["marketValue"]

    model = ARIMA(instrument_data, order=(5, 1, 0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=12)

    return forecast


# Predict market values using LSTM
def lstm_forecast_single(data, instrument_id, target_month=1):
    instrument_data = data[data["instrumentId"] == instrument_id][
        "marketValue"
    ].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    instrument_data = scaler.fit_transform(instrument_data)

    X, y = [], []
    for i in range(len(instrument_data) - (target_month + 1)):
        X.append(instrument_data[i : i + target_month])
        y.append(instrument_data[i + target_month])
    X, y = np.array(X), np.array(y)

    model = Sequential()
    model.add(LSTM(50, activation="relu", input_shape=(target_month, 1)))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=100, batch_size=16)

    input_data = instrument_data[-target_month:]
    input_data = input_data.reshape(1, target_month, 1)

    forecast = model.predict(input_data)
    forecast = scaler.inverse_transform(forecast)

    return forecast[0][0]


def lstm_forecast_multiple(data, instrument_id, forecast_steps=12):
    instrument_data = data[data["instrumentId"] == instrument_id][
        "marketValue"
    ].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    instrument_data = scaler.fit_transform(instrument_data)

    X, y = [], []
    for i in range(len(instrument_data) - (forecast_steps + 1)):
        X.append(instrument_data[i : i + forecast_steps])
        y.append(instrument_data[i + forecast_steps])
    X, y = np.array(X), np.array(y)

    model = Sequential()
    model.add(LSTM(50, activation="relu", input_shape=(forecast_steps, 1)))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=100, batch_size=16)

    forecast_values = []
    input_data = instrument_data[-forecast_steps:]

    for _ in range(forecast_steps):
        input_data_reshaped = input_data.reshape(1, forecast_steps, 1)
        forecast = model.predict(input_data_reshaped)
        forecast = scaler.inverse_transform(forecast)
        forecast_values.append(forecast[0][0])

        input_data = np.roll(input_data, -1)
        input_data[-1] = forecast

    return forecast_values


# Testing
instrument_id = 1
arima_result = arima_forecast(market_values_df, instrument_id)
lstm_result = lstm_forecast_single(market_values_df, instrument_id, target_month=1)
forecasts = lstm_forecast_multiple(market_values_df, instrument_id, forecast_steps=12)

print(f"ARIMA Forecast: {arima_result[-1]}")
print(f"LSTM Forecast: {lstm_result}")
print(f"LSTM Forecast Multiple: {forecasts}")
