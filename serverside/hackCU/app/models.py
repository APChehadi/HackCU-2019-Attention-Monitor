from django.db import models

# Create your models here.


class User(models.Model):
    firstname = models.CharField(max_length = 30)
    lastname = models.CharField(max_length = 30)
    age = models.IntegerField()
    netTimeRatio = models.DecimalField(max_digits = 4, decimal_places = 2)
    netSpeedAverage = models.DecimalField(max_digits = 5, decimal_places = 2)

