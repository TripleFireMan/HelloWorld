# Generated by Django 2.2.6 on 2019-11-21 13:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0003_auto_20191113_0710'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='index',
            field=models.IntegerField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='book',
            name='update_time',
            field=models.DateField(default=datetime.datetime(2019, 11, 21, 13, 31, 23, 565948, tzinfo=utc), max_length=255),
        ),
    ]