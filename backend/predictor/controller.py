# app.py
from flask import Blueprint, request, jsonify
from services import arima_forecast, lstm_forecast, market_values_df

predictor_blueprint = Blueprint("ingestor", __name__)


@predictor_blueprint.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    instrument_id = data.get("instrument_id")

    arima_result = arima_forecast(market_values_df, instrument_id)
    lstm_result = lstm_forecast(market_values_df, instrument_id)

    response = {
        "arima_forecast": arima_result.tolist(),
        "lstm_forecast": lstm_result.tolist(),
    }

    return jsonify(response)
