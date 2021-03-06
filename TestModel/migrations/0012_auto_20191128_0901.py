# Generated by Django 2.2.6 on 2019-11-28 09:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0011_auto_20191122_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='update_time',
            field=models.DateField(default=datetime.datetime(2019, 11, 28, 9, 1, 16, 283278, tzinfo=utc), max_length=255),
        ),
    ]
