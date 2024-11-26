import streamlit as st
import requests
from datetime import datetime
from PIL import Image
from io import BytesIO

# Set the Streamlit page title and layout
st.set_page_config(page_title="Realistic Weather App", page_icon="☀️", layout="centered")

# Set the API key and base URL (replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key)
API_KEY = "661e31209c95328976a7cdc51aebf03f"  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Define a function to get weather data from the API
def get_weather(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"  # Use 'metric' for Celsius, 'imperial' for Fahrenheit
    }
    response = requests.get(BASE_URL, params=params)
    
    # Check if the response was successful
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        st.error("City not found. Please enter a valid city name.")
    else:
        st.error("Unable to retrieve data. Please check your internet connection or try again later.")
    return None

# Set the app header
st.title("☀️ Realistic Weather Information App")
st.write("Enter a city name to get the current weather information.")

# Input section for city name
city_name = st.text_input("🌍 Enter City Name", "")

# When the user enters a city name
if city_name:
    # Fetch weather data from the API
    weather_data = get_weather(city_name)
    
    if weather_data:
        # Extract and display weather information
        st.success(f"Weather information for {city_name.title()}:")

        # Display weather details
        col1, col2 = st.columns([1, 2])

        with col1:
            # Display weather icon
            icon_code = weather_data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
            response = requests.get(icon_url)
            img = Image.open(BytesIO(response.content))
            st.image(img, width=100)

        with col2:
            # Display primary weather info
            main_weather = weather_data["weather"][0]["description"].title()
            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            humidity = weather_data["main"]["humidity"]
            wind_speed = weather_data["wind"]["speed"]
            sunrise = datetime.fromtimestamp(weather_data["sys"]["sunrise"]).strftime("%H:%M:%S")
            sunset = datetime.fromtimestamp(weather_data["sys"]["sunset"]).strftime("%H:%M:%S")
            country = weather_data["sys"]["country"]

            st.markdown(f"**Location**: {city_name.title()}, {country}")
            st.markdown(f"**Weather**: {main_weather}")
            st.markdown(f"**Temperature**: {temp}°C")
            st.markdown(f"**Feels Like**: {feels_like}°C")
            st.markdown(f"**Humidity**: {humidity}%")
            st.markdown(f"**Wind Speed**: {wind_speed} m/s")
            st.markdown(f"**Sunrise**: {sunrise} ⛅️")
            st.markdown(f"**Sunset**: {sunset} 🌇")

        # Additional chart or layout for weather insights
        st.write("---")
        st.write("### Additional Weather Insights")
        st.write(f"- **Temperature**: {temp}°C, **Feels Like**: {feels_like}°C")
        st.write(f"- **Humidity**: {humidity}%, **Wind Speed**: {wind_speed} m/s")

        # Background information for weather condition
        if "rain" in main_weather.lower():
            st.info("🌧️ Don't forget an umbrella! Expect rain today.")
        elif "clear" in main_weather.lower():
            st.info("☀️ It's a clear day! Perfect for outdoor activities.")
        elif "cloud" in main_weather.lower():
            st.info("☁️ It's cloudy. Might be a bit chilly today.")
        elif "snow" in main_weather.lower():
            st.info("❄️ Snowy weather! Stay warm and safe.")
