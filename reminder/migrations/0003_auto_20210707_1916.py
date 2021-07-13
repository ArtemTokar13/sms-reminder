# Generated by Django 3.0 on 2021-07-07 19:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0002_auto_20210706_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remind',
            name='remind',
        ),
        migrations.AddField(
            model_name='remind',
            name='remind_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='remind',
            name='remind_time',
            field=models.TimeField(default=datetime.time(10, 0)),
        ),
    ]
