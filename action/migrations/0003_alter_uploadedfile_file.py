# Generated by Django 4.1.9 on 2023-08-22 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0002_uploadedfile_address_uploadedfile_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
