# Generated by Django 2.2.6 on 2019-11-21 13:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0004_auto_20191121_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='update_time',
            field=models.DateField(default=datetime.datetime(2019, 11, 21, 13, 43, 15, 222662, tzinfo=utc), max_length=255),
        ),
    ]
