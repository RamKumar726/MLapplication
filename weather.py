import requests
import pandas as pd
from datetime import datetime, timedelta

def get_weather_forecast(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'cnt': 56,  # The API returns data for every 3 hours, for 7 days (total 56 data points)
        'appid': api_key,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
        return None

def display_forecast(forecast_data):
    if forecast_data:
        city_name = forecast_data['city']['name']
        forecast_list = forecast_data['list']

        forecast = []

        for item in forecast_list:
            date = datetime.utcfromtimestamp(item['dt'])
            weather = item['weather'][0]['description']
            temp = item['main']['temp']
            forecast.append([date, weather, temp])
        
        df = pd.DataFrame(forecast, columns=['Date', 'Weather', 'Temperature (°C)'])
        
        # Group by date and calculate the average temperature and mode weather description
        df['Date'] = df['Date'].dt.date  # Convert datetime to date
        daily_forecast = df.groupby('Date').agg({
            'Temperature (°C)': 'mean',
            'Weather': lambda x: x.mode()[0]  # Get the most frequent weather description
        }).reset_index()

        print(f"Weather forecast for {city_name} for the next 7 days:")
        print(daily_forecast)
        return daily_forecast
    else:
        print("No forecast data to display")
        return None

def weather(city):
    api_key = "da66f1a51ff1a0db062cc5cf54b05cb8"  # Replace with your actual OpenWeatherMap API key
    forecast_data = get_weather_forecast(city, api_key)
    return display_forecast(forecast_data)
