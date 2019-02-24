from django.db import models

# Create your models here.


class User(models.Model):
    #basics
    firstname = models.CharField(max_length = 30)
    lastname = models.CharField(max_length = 30)
    age = models.IntegerField()

    #eyes on road / eyes off road
    netTimeRatio = models.DecimalField(max_digits = 4, decimal_places = 2)

    #average speed
    netSpeedAverage = models.DecimalField(max_digits = 5, decimal_places = 2)

    driving = models.BooleanField(default = False)

    #number of drives
    drives = models.IntegerField()



    def __str__(self):
        return self.firstname

