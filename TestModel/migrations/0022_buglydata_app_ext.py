# Generated by Django 2.2.6 on 2020-12-13 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0021_buglydata'),
    ]

    operations = [
        migrations.AddField(
            model_name='buglydata',
            name='app_ext',
            field=models.CharField(default='', max_length=255),
        ),
    ]