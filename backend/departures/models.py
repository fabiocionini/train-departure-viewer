from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.code)

class Departure(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="")  # id for train, needed for updates
    planned_time = models.DateTimeField('planned departure time')
    direction = models.CharField(max_length=200)
    platform = models.CharField(max_length=10)
    train_type = models.CharField(max_length=50)

    def __str__(self):
        return '{0} {1} {2} - Platform {3}'.format(self.planned_time, self.train_type, self.direction, self.platform)
