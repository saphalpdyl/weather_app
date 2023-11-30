import os
import requests
import json

from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

class MainView(View) : 
    def get(self, request: HttpRequest) :
        city_name = request.GET.get('city', None)

        if city_name :
            weather_api_key = os.environ.get('WEATHER_API_KEY')

            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_api_key}&units=Metric'
            weather_response = requests.get(url).json()

            context = {}
            
            if weather_response['cod'] == 200 : 
                temp = round(weather_response['main']['temp'])  
                weather = weather_response['weather']
                coords = weather_response['coord']
                wind = weather_response['wind']
                humidity = weather_response['main']['humidity']
            
                description = weather_response['weather'][0]['description']
                print(coords['lat'])

                # Sending Http POST request for air quality index to Google Maps API
                maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
                url = f'https://airquality.googleapis.com/v1/currentConditions:lookup?key={maps_api_key}'
                maps_params = {
                    "location" : {
                        "longitude" : coords['lon'],
                        "latitude" : coords['lat']
                    }
                }
                # air_quality_response = requests.post(url, data=json.dumps(maps_params)).json()
                

                context = {
                    "temp" : temp,
                    "weather" : weather[0] ,
                    "description" : description,
                    "coords" : coords,
                    "wind" : wind,
                    "humidity" : humidity,
                    # "aqi" : air_quality_response['indexes'][0]

                }
            else :
                return redirect(reverse_lazy('main'))

            return render(request, 'weather_app/main.html', context)
        else : 
            return render(request, 'weather_app/search.html')
        