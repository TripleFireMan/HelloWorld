# Generated by Django 2.2.6 on 2019-11-13 06:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='update_time',
            field=models.DateField(default=datetime.datetime(2019, 11, 13, 6, 28, 51, 891172, tzinfo=utc), max_length=255),
        ),
    ]