# Generated by Django 3.1 on 2023-06-20 15:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('TYMetro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(blank=True, default=django.utils.timezone.now, max_length=255, verbose_name='生日'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='introduce',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name='个人简介'),
        ),
    ]
