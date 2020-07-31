from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm
from django.contrib import messages
import requests
from django.contrib import messages
# Create your views here.
def home(request):
    api_url="http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=b5123596d3e46ebe5afd8c09b0c848f0"
    if request.method=="POST":
        form = CityForm(request.POST)
        if form.is_valid():
            print("is valid")
            cn=form.cleaned_data.get('name')
            json_data=requests.get((api_url).format(cn)).json()
            if json_data["cod"]==200:
                if City.objects.filter(name=cn).count==0:
                    form.save()
                    messages.success(request,f'Welcome')
                    return redirect('home')
                else:
                    messages.info(request,f'Already exists')
                    return redirect('home')
            else:
                messages.error(request,f'Invalid city')
                return redirect('home')
    else:
        form = CityForm()
        print("is not valid")
    cities=City.objects.all()
    weather_data=[]
    
    cities=City.objects.all()
    for city in cities:
        json_data=requests.get((api_url).format(city)).json()
        fd=json_data['weather'][0]['main']
        print(fd)
        city_data={
                'name':city.name,
                'icon':json_data['weather'][0]['icon'],
                'temperature':json_data['main']['temp'],
                'description':json_data['weather'][0]['description'],
        }
        weather_data.append(city_data)
    return render(request, 'weather/home.html',{'form':form,'weather_data':weather_data})

def deletecity(request,city_name):
    c=City.objects.get(name=city_name)
    c.delete()
    return redirect('home')
