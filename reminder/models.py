import datetime


from django.contrib.auth.models import User
from django.db import models


class Remind(models.Model):
    title = models.CharField(max_length=100)
    remind_date = models.DateField(default=datetime.date.today)
    remind_time = models.TimeField(default=datetime.time(10, 0))
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class RemindUser(models.Model):
    phonenumber = models.CharField(max_length=50)
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)
