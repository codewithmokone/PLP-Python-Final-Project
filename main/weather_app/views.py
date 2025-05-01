import json
import urllib.request
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&appid=2c30634243f65ad7130c3c5dba70dd9a').read()

        list_of_data = json.loads(source)

        data = {
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
        print(data)
    else:
        data = {}

    return render(request, 'index.html', data)