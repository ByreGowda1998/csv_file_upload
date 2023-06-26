from django.db import models
from usersapp.models import TimeStampModel
# Create your models here.
from django.db import models
from datetime import datetime

def get_csv_upload_path(instance, filename):
    now=datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
    print("date and time:",date_time)	
    return f'{date_time}/{filename}'




class CsvFileUpload(TimeStampModel):
    csv_file = models.FileField(upload_to=get_csv_upload_path)
    upload_status = models.IntegerField(default=0) # 0=to-be-processed, 1=processing, 2=error, 3=done
    message = models.CharField('Message', max_length=255, blank=True, null=True)

    
def __unicode__(self):
    file_name = self.csv_file
    return file_name