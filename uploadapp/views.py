from django.shortcuts import render,redirect
import csv
from django.contrib.auth import get_user_model
User=get_user_model()
from uploadapp.forms import CsvUploadForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from uploadapp.data_processor import  procees_csvfile
from uploadapp.models import CsvFileUpload,CsvProcessedfile
from django.contrib import messages
import pandas as pd
import mimetypes
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.shortcuts import render, get_object_or_404



# def upload_csv(request):
   
#     if request.method == 'POST':
#         form = CsvUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.email = request.user.email
#             form.save() 
#             pathname=form.cleaned_data["csv_file"].name
#             csv_file=form.cleaned_data["csv_file"].name.replace(' ','_')
#             procees_csvfile(csv_file,pathname)
#             messages.success(request,f"File  {pathname} is uploadded succesfully")
#             return redirect('lis_files')
#         else:
#            error=form.errors
#            messages.errors(request,f"File    {pathname} is Not able to Uploaded Bcause of {error}")
#     form = CsvUploadForm()
#     return render(request, 'uploadcsv.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.email: 
                obj.email = request.user.email 
            form.save()
            pathname = form.cleaned_data["csv_file"].name
            csv_file = form.cleaned_data["csv_file"].name.replace(' ', '_')
            procees_csvfile(csv_file, pathname)
            messages.success(request, f"File {pathname} is uploaded successfully")
            return redirect('list_files')
        else:
            error = form.errors
            messages.errors(request, f"File {pathname} is not able to be uploaded because of {error}")
    else:
        form = CsvUploadForm(initial={'email': request.user.email})  
    return render(request, 'uploadcsv.html', {'form': form})




def listprocssedfile(request):
    processdcsv_file=CsvProcessedfile.objects.all().order_by('-created_at')
    
    return render (request,'list_processed_file.html',{"processed_file":processdcsv_file})







def view_data(request, pk):
    if pk:
        file_path = get_object_or_404(CsvProcessedfile, pk=pk)
        csv_path = file_path.processed_file.path

        no_of_cols = 56

        df = pd.read_csv(csv_path, skiprows=7, usecols=[i for i in range(no_of_cols)], skipfooter=1, engine='python')

        with open(csv_path, 'r') as file:
            csv_data = file.readlines()

        sentences = csv_data[:6]

        table = df.to_html()

       
       

        context = {'table': table ,'sentences': sentences,}
        return render(request, 'listdata.html', context)
    else:
        print("No file present")







def download_data(request, pk):
    if pk:
        file_path = get_object_or_404(CsvProcessedfile, pk=pk)
        csv_path = file_path.processed_file.path
        
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_path.processed_file.name)
        
        with open(csv_path, 'rb') as file:
            response.write(file.read())
        
        return response
    else:
        print("No file present")



