# Generated by Django 3.1 on 2020-09-23 08:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0008_tasks_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivered',
            name='delivered_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='delivered',
            name='delivered_time',
            field=models.TimeField(default=datetime.datetime(2020, 9, 23, 8, 30, 14, 203854, tzinfo=utc)),
        ),
    ]
