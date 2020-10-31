# Generated by Django 3.1 on 2020-09-25 14:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0016_auto_20200925_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='return_documents',
            name='task_id',
        ),
        migrations.AlterField(
            model_name='delivered',
            name='delivered_time',
            field=models.TimeField(default=datetime.datetime(2020, 9, 25, 14, 41, 28, 282039)),
        ),
        migrations.AlterField(
            model_name='returned',
            name='returned_time',
            field=models.TimeField(default=datetime.datetime(2020, 9, 25, 14, 41, 28, 282039)),
        ),
    ]