# Generated by Django 4.2.2 on 2023-06-27 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadapp', '0004_csvfileupload_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvfileupload',
            name='in_time',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='csvfileupload',
            name='out_time',
            field=models.CharField(max_length=10),
        ),
    ]