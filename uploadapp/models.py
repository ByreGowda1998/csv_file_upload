from django.db import models
from usersapp.models import TimeStampModel
# Create your models here.
from django.db import models
from datetime import datetime


def get_csv_upload_path(instance, filename):
    # now=datetime.now()
    # date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
    # print("date and time:",date_time)
    return f'{filename}'








class CsvFileUpload(TimeStampModel):
    csv_file = models.FileField(upload_to=get_csv_upload_path,max_length=600)
    in_time= models.CharField(max_length=10 )
    out_time=models.CharField(max_length=10)
    email=models.EmailField()

   
    def __str__(self):
        file_name = self.csv_file.name.split('/')[0]
        return file_name