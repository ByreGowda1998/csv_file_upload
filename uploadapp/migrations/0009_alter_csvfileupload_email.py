# Generated by Django 4.2.2 on 2023-07-03 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadapp', '0008_csvfileupload_unique_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvfileupload',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
    ]
