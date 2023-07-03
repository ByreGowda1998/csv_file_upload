from django.db import models
from usersapp.models import TimeStampModel
# Create your models here.
from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
import uuid
user=get_user_model()

def get_csv_upload_path(instance, filename):
    # now=datetime.now()
    # date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
    # print("date and time:",date_time)
    return f'{filename}'


from django.utils import timezone

def generate_time_choices():
    current_time = timezone.now()
    time_choices = []

    for hour in range(24):
        time = current_time.replace(hour=hour, minute=0).strftime('%H:%M')
        time_choices.append((time, time))
    return time_choices







class CsvFileUpload(TimeStampModel):
    Time_Choice=generate_time_choices()
    csv_file = models.FileField(upload_to=get_csv_upload_path,max_length=600)
    in_time= models.CharField(max_length=20 ,choices=Time_Choice)
    out_time=models.CharField(max_length=20,choices=Time_Choice)
    email=models.EmailField(default='')


    

    def __str__(self):
        file_name = self.csv_file.name.split('/')[0]
        return file_name
    
def get_processed_csv_upload_path(instance,filename):
    now=datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
    print("date and time:",date_time)
    return f'{date_time}/{filename}'

  


class CsvProcessedfile(TimeStampModel):
    csv_processed_file =models.ForeignKey(CsvFileUpload, on_delete=models.CASCADE ,blank=False)
    processed_file = models.FileField(upload_to=get_processed_csv_upload_path,max_length=600,blank=False)



    def __str__(self):
        csv_processed_file = self.csv_processed_file  
        return csv_processed_file.csv_file.name



