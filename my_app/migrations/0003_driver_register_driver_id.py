# Generated by Django 3.1 on 2020-09-08 05:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_driver_register'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver_register',
            name='driver_id',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=6, unique=True),
        ),
    ]
