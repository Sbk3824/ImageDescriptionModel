from django.db import models

# Create your models here.

class Image(models.Model):
    #title = models.CharField(max_length=255, blank=True)
    file = models.ImageField('img', upload_to='Images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
