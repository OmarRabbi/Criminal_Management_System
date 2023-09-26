from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CriminalRecords(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    criminal_name = models.CharField(max_length=100)
    age = models.IntegerField()
    height = models.FloatField()
    unique_identity = models.CharField(max_length=200)
    criminal_image = models.ImageField(upload_to="criminal_image")
    crime_type = models.CharField(max_length=200)
    crime_desc = models.TextField()
    