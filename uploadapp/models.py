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
    Time_Choice=generate_time_choices()
    csv_file = models.FileField(upload_to=get_csv_upload_path,max_length=600)
    in_time= models.CharField(max_length=20 ,choices=Time_Choice)
    out_time=models.CharField(max_length=20,choices=Time_Choice)
    email=models.EmailField(default='')

  

   
    def __str__(self):
        file_name = self.csv_file.name.split('/')[0]
        return file_name
    

    def save(self, *args, **kwargs):
        if not self.email:
            # Set the default email as the current logged-in user's email
            self.email = get_user_model().objects.get(username=self.user).email
        super().save(*args, **kwargs)
    


class CsvProcessedfile(TimeStampModel):
    csv_proccessed_file =models.ForeignKey(CsvFileUpload, on_delete=models.CASCADE ,blank=False)
    file_name=models.CharField(max_length=400,blank=False)
    proccedfile_path = models.CharField(max_length=600,blank=False,)



    def __str__(self):
        return self.file_name



