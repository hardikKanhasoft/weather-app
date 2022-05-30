import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=010721642521f31b0fbc8c3831d45951'

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name = new_city).count()
            
            if existing_city_count == 0:
                # if r['cod'] == 200:
                    form.save()
            #     else :
            #         err_msg = 'City does not exist in this world!'
            # else: 
            #    err_msg = 'City already exists in database!'
               
            
    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
        print(r)

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'temperature_C' : round((r['main']['temp'] - 32 )* (5/9)),
            'description' : r['weather'][0]['description'], 
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)
        print(weather_data)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)