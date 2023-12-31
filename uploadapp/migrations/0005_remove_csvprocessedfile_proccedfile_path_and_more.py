# Generated by Django 4.2.2 on 2023-07-03 07:46

from django.db import migrations, models
import uploadapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadapp', '0004_alter_csvfileupload_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csvprocessedfile',
            name='proccedfile_path',
        ),
        migrations.AddField(
            model_name='csvprocessedfile',
            name='processed_file_path',
            field=models.FileField(default=' ', max_length=600, upload_to=uploadapp.models.get_processed_csv_upload_path),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='csvprocessedfile',
            name='file_name',
            field=models.CharField(max_length=600),
        ),
    ]
