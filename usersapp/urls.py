from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('' ,views.homepage,name ='home'),
    path('loginto/',views.loginto,name='loginto'),
    path('logout/',views.log_out,name="logout"),
  
    
    
]