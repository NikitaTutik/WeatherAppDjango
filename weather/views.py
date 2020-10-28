from django.shortcuts import render, redirect
from .models import *
from .forms import *
import requests
from .models import WeatherModel
from django.contrib import messages


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=API_ID'
    cities = WeatherModel.objects.all()
    weather_data = []
    error_msg = ''
    if request.method == "POST":
        form = WeatherForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['city']
            ex_city = WeatherModel.objects.filter(city=new_city).count()
            if ex_city == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    messages.error(request, 'City does not exist!')
            else:
                messages.error(request, 'City already exists!')
    else:
        form = WeatherForm()

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)


def delete_city(request, city):
    WeatherModel.objects.get(city=city).delete()

    return redirect('index')
