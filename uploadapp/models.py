from django.db import models
from usersapp.models import TimeStampModel
# Create your models here.
from django.db import models
from datetime import datetime

def get_csv_upload_path(instance, filename):
    now=datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
    print("date and time:",date_time)
    folder ="Uploadedfiles"
    return f'{folder}/{date_time}/{filename}'





class CsvFileUpload(TimeStampModel):
    csv_file = models.FileField(upload_to=get_csv_upload_path,max_length=600)
    upload_status = models.IntegerField(default=0) 
    message = models.CharField('Message', max_length=255, blank=True, null=True)

    
    def __str__(self):
        file_name = self.csv_file.name.split('/')[2]
        return file_name