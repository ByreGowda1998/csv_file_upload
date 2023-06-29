from django import forms
from django.contrib.auth import get_user_model
User=get_user_model()
from django.forms import ModelForm
from uploadapp.models import CsvFileUpload



class CsvUploadForm(ModelForm):
    class Meta:
        model = CsvFileUpload
        fields = ("csv_file","in_time","out_time","email")
        widgets = {
            'my_choice': forms.Select(attrs={'class': 'custom-select'}),
        }