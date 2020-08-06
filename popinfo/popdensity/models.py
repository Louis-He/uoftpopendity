from django.db import models

# Create your models here.
class Connrecord(models.Model):
    recordtime = models.DateTimeField('record time')
    location = models.IntegerField(default=-1)
    conn = models.IntegerField(default=-1)
