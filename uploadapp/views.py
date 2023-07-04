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
from django.contrib.auth.decorators import login_required


def check_csv_file():
    pass




@login_required(login_url='login')
def upload_csv(request):
   
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            if len(obj.email)==0:
                obj.email=request.user.email
            form.save() 
            pathname=form.cleaned_data["csv_file"].name
            csv_file=form.cleaned_data["csv_file"].name.replace(' ','_')
            procees_csvfile(csv_file,pathname)
            messages.success(request,f"File  {pathname} is uploadded succesfully")
            return redirect('list_files')
        else:
           error=form.errors
           messages.errors(request,f"File    {pathname} is Not able to Uploaded Bcause of {error}")
    form = CsvUploadForm()
    return render(request, 'uploadcsv.html', {'form': form})




@login_required(login_url='login')
def listprocssedfile(request):
    processed_csv_file=CsvProcessedfile.objects.all().order_by('-created_at')
    return render (request,'list_processed_file.html',{"processed_file":processed_csv_file})






@login_required(login_url='login')
def view_data(request, pk):
    if pk:
        file_path = get_object_or_404(CsvProcessedfile, pk=pk)
        csv_path = file_path.processed_file.path

        split_path=csv_path.split('/')
       
        split_path.insert(8,'processed')
       
        new_path='/'.join(split_path)
       

        no_of_cols = 56

        df = pd.read_csv(new_path, skiprows=7, usecols=[i for i in range(no_of_cols)], skipfooter=2, engine='python')

        with open(new_path, 'r') as file:
            csv_data = file.readlines()

        sentences = csv_data[:6]

        table = df.to_html()

        context = {'table': table ,'sentences': sentences,}
        return render(request, 'listdata.html', context)
    else:
        messages.error("File your downloading not present")



@login_required(login_url='login')
def download_data(request, pk):
    if pk:
        file_path = get_object_or_404(CsvProcessedfile, pk=pk)
        csv_path = file_path.processed_file.path
        split_path=csv_path.split('/')
        split_path.insert(8,'processed')
        new_path='/'.join(split_path)
      
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_path.processed_file.name)
        
        with open(new_path, 'rb') as file:
            response.write(file.read())
        
        return response
    else:
        messages.error("File your downloading not present")



