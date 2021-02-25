from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('deletecity/<str:cityname>',views.deletecity,name='deletecity'),
    path('xcelexport/',views.xcelexport,name='xcelexport'),
    path('sendemail/',views.sendemail,name='sendemail'),
]
