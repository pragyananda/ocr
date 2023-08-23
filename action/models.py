from django.db import models

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='')
    name = models.CharField( max_length=30,default='none')
    dob = models.CharField( max_length=30,default='none')
    mobile = models.CharField( max_length=30,default='none')
    address = models.CharField( max_length=100,default='none')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    finalized = models.BooleanField(default=False)
