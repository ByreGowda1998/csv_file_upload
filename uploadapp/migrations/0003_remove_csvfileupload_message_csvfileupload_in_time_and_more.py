# Generated by Django 4.2.2 on 2023-06-27 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadapp', '0002_alter_csvfileupload_csv_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csvfileupload',
            name='message',
        ),
        migrations.AddField(
            model_name='csvfileupload',
            name='in_time',
            field=models.CharField(default='12:00', max_length=10),
        ),
        migrations.AddField(
            model_name='csvfileupload',
            name='out_time',
            field=models.CharField(default='12:00', max_length=10),
        ),
    ]
