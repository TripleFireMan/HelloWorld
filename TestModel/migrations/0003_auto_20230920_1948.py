# Generated by Django 3.1.4 on 2023-09-20 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0002_delete_tag'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]