from django.db import models

# Create your models here.

class app_auth_token_tb(models.Model):
    token                    = models.CharField(max_length=100,default='')
    created_at               = models.DateTimeField(max_length=100,default='')
    updated_at               = models.DateTimeField(max_length=100,default='')
    
class pdf_data_tb(models.Model):
    pdf_file                 = models.FileField(upload_to='pdf',null=True)
    created_at               = models.DateTimeField(max_length=100,default='')
    updated_at               = models.DateTimeField(max_length=100,default='')

class pdf_to_image_data_tb(models.Model):
    pdf_id                   = models.ForeignKey(pdf_data_tb,on_delete=models.CASCADE,default='',null=True)
    title                    = models.CharField(max_length=100,default='')
    image                    = models.FileField(upload_to='pdf_images',null=True)
    created_at               = models.DateTimeField(max_length=100,default='')
    updated_at               = models.DateTimeField(max_length=100,default='')  