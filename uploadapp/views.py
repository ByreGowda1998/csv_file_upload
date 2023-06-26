from django.shortcuts import render,redirect
import csv
from django.contrib.auth import get_user_model
User=get_user_model()
from uploadapp.forms import CsvUploadForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def upload_csv(request):
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'base.html') 
    else:
        form = CsvUploadForm()
    return render(request, 'uploadcsv.html', {'form': form})

