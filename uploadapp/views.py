from django.shortcuts import render,redirect
import csv
from django.contrib.auth import get_user_model
User=get_user_model()
from uploadapp.forms import CsvUploadForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from uploadapp.data_processor import  procees_csvfile
from uploadapp.models import CsvFileUpload


def upload_csv(request):
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            pathname=form.cleaned_data["csv_file"].name
            csv_file=form.cleaned_data["csv_file"].name.replace(' ','_')
            procees_csvfile.delay(csv_file,pathname)
            return render(request, 'base.html') 
        else:
           print(form.errors)
    form = CsvUploadForm()
    return render(request, 'uploadcsv.html', {'form': form})

