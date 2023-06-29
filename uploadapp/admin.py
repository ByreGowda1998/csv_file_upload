from django.contrib import admin
from .models import CsvFileUpload,CsvProcessedfile
#Register your models here.
admin.site.register(CsvFileUpload)

admin.site.register(CsvProcessedfile)