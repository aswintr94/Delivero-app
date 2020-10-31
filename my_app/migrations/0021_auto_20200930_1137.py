# Generated by Django 3.1 on 2020-09-30 11:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0020_auto_20200928_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivered',
            name='delivered_time',
            field=models.TimeField(default=datetime.datetime(2020, 9, 30, 11, 37, 2, 410279)),
        ),
        migrations.AlterField(
            model_name='delivery_docs_by_admin',
            name='task_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.delivered'),
        ),
        migrations.AlterField(
            model_name='returned',
            name='returned_time',
            field=models.TimeField(default=datetime.datetime(2020, 9, 30, 11, 37, 2, 410279)),
        ),
    ]
