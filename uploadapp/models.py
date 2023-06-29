from django.db import models
from usersapp.models import TimeStampModel
# Create your models here.
from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()

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
    # uniq_file_id = models.UUIDField(
    #      primary_key = True,
    #      default = uuid.uuid4,
    #      editable = False)
    Time_Choice=generate_time_choices()
    csv_file = models.FileField(upload_to=get_csv_upload_path,max_length=600)
    in_time= models.CharField(max_length=20 ,choices=Time_Choice)
    out_time=models.CharField(max_length=20,choices=Time_Choice)
    email=models.EmailField()

  

   
    def __str__(self):
        file_name = self.csv_file.name.split('/')[0]
        return file_name