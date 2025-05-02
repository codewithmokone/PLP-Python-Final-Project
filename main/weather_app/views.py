# Import necessary modules
import json # For parsing JSON data
import geocoder # Retrieving geo-location
import urllib.request # Making  HTTP requests
from django.shortcuts import render # Rendering templates

# OpenWeather API KEY
API_KEYS = 'd419b9f7c89a51567c00f107799af646'

# Function for fetching weather data from API URL
def fetch_weather_data(url):
    try:
        # HTTP request and read the response
        source = urllib.request.urlopen(url).read()
        ## Parse JSON response into a Python dictionary
        list_of_data = json.loads(source)

        # Extract and return weather data 
        return {
            'name': str(list_of_data['name']),
            'main': str(list_of_data['weather'][0]['main']),
            'country_code': str(list_of_data['sys']['country']),
            'coordinate': str(list_of_data['coord']['lon']) + ', '
            + str(list_of_data['coord']['lat']),
            'icon': list_of_data['weather'][0]['icon'],
            'temp': str(int(list_of_data['main']['temp'])) + '°',
            'clouds': str(list_of_data['clouds']['all']),
            'humidity': str(list_of_data['main']['humidity']),
            'wind': str(list_of_data['wind']['speed']),
        }

    except Exception as e:
        # Handles eror and print the error for debugging
        print(f"Error fetching weather data: {e}")
        return {}

# Django view function to handle weather display logic
def index(request):
    if request.method == 'POST':
        # If the request is POST, get city name from the input
        city = request.POST['city']
        # API URL using city name
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEYS}"
        print("url", url)
        # Fetch weather data for the provided city
        data = fetch_weather_data(url)
        print("Searched location: ", data)
    else:
        # If not POST, attempt to use IP geolocation
        g = geocoder.ip('me') # Get location info from IP address
        print(g)
        if g.latlng:
            # If coordinates found, construct API URL using them
            lat, lon = g.latlng
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEYS}"
            # Fetch weather data based on IP location
            data = fetch_weather_data(url)
            print("Geo Data: ", data)
        else:
            # If geolocation fails, return empty data
            data = {}

    # Render the index.html template with the weather data
    return render(request, 'index.html', {'data': data})