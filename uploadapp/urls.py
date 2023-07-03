from django.contrib import admin
from django.urls import path
from  uploadapp import views

urlpatterns = [
   
   path('upload_csv/' ,views.upload_csv,name = 'upload_csv'),
   path('procced_csv/',views.listprocssedfile,name='list_files'),
   path('view_data/<int:pk>/',views.view_data, name='view_data'),
   path('data/download/<int:pk>/',views.download_data, name='download_data'),
    
]