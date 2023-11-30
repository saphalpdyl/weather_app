import os
import requests
import json

from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

class MainView(View) : 
    def get(self, request: HttpRequest) :
        city_name = request.GET.get('city', None)
        context = {
            "is_available" : False
        }

        if city_name :
            weather_api_key = os.environ.get('WEATHER_API_KEY')

            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_api_key}&units=Metric'
            weather_response = requests.get(url).json()

            if weather_response['cod'] == 200 : 
                temp = round(weather_response['main']['temp'])
                temp_data = weather_response['main']
                weather = weather_response['weather']
                coords = weather_response['coord']
                wind = weather_response['wind']
            
                description = weather_response['weather'][0]['description']

                # Sending Http POST request for air quality index to Google Maps API
                maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
                url = f'https://airquality.googleapis.com/v1/currentConditions:lookup?key={maps_api_key}'
                maps_params = {
                    "location" : {
                        "longitude" : coords['lon'],
                        "latitude" : coords['lat']
                    }
                }
                air_quality_response = requests.post(url, data=json.dumps(maps_params)).json()
                aqi_exists = False
                aqi_colors = {}

                if air_quality_response.get('error') :
                    aqi = "Not Available"
                else :
                    aqi = air_quality_response['indexes'][0]['aqiDisplay']
                    aqi_colors_unadjusted = air_quality_response['indexes'][0]['color']
                    aqi_red = aqi_colors_unadjusted.get('red',0) * 255
                    aqi_blue = aqi_colors_unadjusted.get('blue',0) * 255
                    aqi_green = aqi_colors_unadjusted.get('green',0) * 255
                    aqi_colors = {
                        "red" : aqi_red,
                        "blue" : aqi_blue,
                        "green" : aqi_green,
                    }
                    aqi_exists = True

                context = {
                    "is_available" : True,
                    "temp" : temp,
                    "temp_data" : temp_data,
                    "weather" : weather[0] ,
                    "description" : description,
                    "coords" : coords,
                    "wind" : wind,
                    "aqi" : aqi,
                    "loc" : city_name,
                    "aqi_exists" : aqi_exists,
                    "aqi_colors" : aqi_colors
                }

        return render(request, 'weather_app/search.html', context)