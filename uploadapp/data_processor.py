

# import the corresponding modules
from celery import shared_task
from django.core.mail import EmailMessage
import pandas as pd
import csv 
from uploadapp.models import CsvFileUpload,CsvProcessedfile
import os
from csv_upload_project import settings
import datetime
from  csv_upload_project.settings import BASE_DIR
from pathlib import Path
from datetime import datetime
now=datetime.now()
date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
from django.contrib import messages



def return_email(request):
    print(request.user)


@shared_task(name='process_csvfile')
def procees_csvfile(filename=None,pathname=None):
    if filename and pathname:
        file = CsvFileUpload.objects.filter(csv_file__endswith=filename).first()
        print(file.in_time,file.out_time,type(file.in_time))
        
        if file:
            file_path = file.csv_file.path                                   
            absolute_file_path = os.path.join(settings.MEDIA_ROOT,file_path)

          
            no_of_cols = 56                                                                                   
                                                                                                   
            df = pd.read_csv(f'{absolute_file_path}', skiprows=7, usecols=[i for i in range(no_of_cols)])     

            df_with_extra_data= pd.read_csv(f'{absolute_file_path}', header=None, nrows=6, names=range(2))   
            
            
           
            IN_TIME = file.in_time                                                                        
            OUT_TIME = file.out_time      



            omitted_columns =[0,1,2,3,4,5,6,7]
            omitted_df = df[df.columns[omitted_columns]]
            df = df.iloc[:-1, 8:57]
            columns = df.columns[(df.columns >=IN_TIME) & (df.columns <= OUT_TIME)]
            columns_out = df.columns[(df.columns <IN_TIME) | (df.columns > OUT_TIME)]
            df['SumOutsideRange'] = df[columns].sum(axis=1)

            # Compute the sum for each row outside the time range.
            df['SumWithinRange'] = df[columns_out].sum(axis=1)

            # Calculate percentages based on the sums and total time
            df['PercentageWithinRange'] = (df['SumWithinRange'] / df.sum(axis=1)) * 100
            df['PercentageOutsideRange'] = (df['SumOutsideRange'] / df.sum(axis=1)) * 100

            # Calculate statistics for columns within the range.
            df['Min_within_range'] = df[columns].min(axis=1)
            df['Max_within_range'] = df[columns].max(axis=1)
            df['Avg_within_range'] = df[columns].mean(axis=1)

            # Calculate statistics for columns outside the range.
            df['Min_outside_range'] = df[columns_out].min(axis=1)
            df['Max_outside_range'] = df[columns_out].max(axis=1)
            df['Avg_outside_range'] = df[columns_out].mean(axis=1)

            # Round the decimal value to 3 points.
            rounded_df = df.round(3)
            merged_df = pd.concat([ omitted_df, rounded_df], axis=1)
            df_no_na = df_with_extra_data.fillna('')

            path=BASE_DIR/"media"/"processed"

            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)
            file_name = pathname.replace(".csv",f"_processed@{date_time}.csv")
            file_path = BASE_DIR/"media"/"processed"/file_name
           
            email_to=[f"{file.email}"]

            print(email_to,"these my email")
            with open(file_path, 'w',newline='') as f:
                writer = csv.writer(f)
                for index,row in df_no_na.iterrows():
                    writer.writerow(row)
                writer.writerow("\n")
                write_index = True
                for index1,row1 in merged_df.iterrows():
                    if write_index:
                        writer.writerow(row1.index)
                        write_index=False
                    else:
                        writer.writerow(row1)


        
            csv_processed_file = CsvProcessedfile(csv_processed_file=file, processed_file=file_name )
            csv_processed_file.save()
   

      

            message = EmailMessage(
            "Subject",
            f"{pathname} is proceed ",
            "From@example.com",
            email_to,
                )
            with open(file_path, 'rb') as file:
                message.attach(file_name, file.read(), 'text/csv')
                message.send(fail_silently=False)

        
        else:
            message.errors(f"File {file_name} not present in database")

    else:
        message.error(f"No file  present in daybase with these filename {file_name}")       


