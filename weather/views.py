from django.shortcuts import render
from . import views
from .forms import CityForm
import requests
import csv
from .models import City
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.mail import send_mail as sm



def index(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=1ed51c0feea73a70d2868d2566edce08'
    #city='Las Vegas'
    #state='702'
    if request.method == "POST":
        form=CityForm(request.POST)
        form.save()
    form=CityForm()
    weather_data=[]
    cities=City.objects.all()
    for city in cities:
        r=requests.get(url.format(city)).json()
        #print(r.text)
        city_data={'desc' : r['weather'][0]['description'],
        'city':city.name,
        'icon':r['weather'][0]['icon'],
        'temp':r['main']['temp']
        }
        weather_data.append(city_data)
    page=request.GET.get('page',1)
    paginator=Paginator(weather_data,3)
    try:
        city_weathers=paginator.page(page)
    except PageNotAnInteger:
        city_weathers=paginator.page(1)
    except EmptyPage:
        city_weathers=paginator.page(paginator,num_pages)
    return render(request,'weather/weather.html',{'city_weathers':city_weathers,'form':form})


def deletecity(request,cityname):
    city_delete=City.objects.filter(name=cityname).delete()
    if request.method == "POST":
        form=CityForm(request.POST)
        form.city_delete.delete()
        form.save()
    return HttpResponseRedirect(reverse("index"))


def xcelexport(request):
    response=HttpResponse(content_type='text/csv')
    writer=csv.writer(response)
    writer.writerow(['name'])
    for c in City.objects.all():
        writer.writerow([c.name])
    response['Content-Disposition']='attachment; filename="city.csv"'
    return response


def sendemail(request):
    res = sm(
        subject = 'Subject here',
        message = 'Here is the message.',
        from_email = 'gomathirajendran@gmail.com',
        recipient_list = ['gomathisureshfine@gmail.com'],
        fail_silently=False,
    )    

    return HttpResponse(f"Email sent to {res} members")
