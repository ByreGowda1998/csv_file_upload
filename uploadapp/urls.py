from django.contrib import admin
from django.urls import path
from  uploadapp import views

urlpatterns = [
   
   path('upload_csv/' ,views.upload_csv,name = 'upload_csv'),
   path('procced_csv/',views.listprocssedfile,name='lis_files')
    
]