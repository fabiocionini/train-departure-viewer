# Generated by Django 3.1.7 on 2021-04-04 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departures', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='departure',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
