from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)

class Departure(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    planned_time = models.DateTimeField('planned departure time')
    direction = models.CharField(max_length=200)
    platform = models.CharField(max_length=10)
    train_type = models.CharField(max_length=50)
