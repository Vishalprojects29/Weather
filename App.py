from flask import Flask, request, jsonify # type: ignore
import requests # type: ignore
from flask_cors import CORS  # type: ignore
app = Flask(__name__)
CORS(app)
API_KEY = "0a3b992dd39f1886d839f7fd1760b8e2"  
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_API_URL = "https://api.openweathermap.org/data/2.5/forecast"
AIR_QUALITY_API_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    lang = request.args.get('lang', 'en')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': lang
    }
    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()
        return jsonify(weather_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
@app.route('/forecast', methods=['GET'])
def get_forecast():
    city = request.args.get('city')
    lang = request.args.get('lang', 'en')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': lang
    }
    try:
        response = requests.get(FORECAST_API_URL, params=params)
        response.raise_for_status()
        forecast_data = response.json()
        return jsonify(forecast_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
@app.route('/air_quality', methods=['GET'])
def get_air_quality():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {
        'q': city,
        'limit': 1,
        'appid': API_KEY
    }
    try:
        geo_response = requests.get(geocoding_url, params=geo_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        if not geo_data:
            return jsonify({"error": "City not found"}), 404
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        aq_params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY
        }
        aq_response = requests.get(AIR_QUALITY_API_URL, params=aq_params)
        aq_response.raise_for_status()
        air_quality_data = aq_response.json()
        return jsonify(air_quality_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
