# Generated by Django 3.0.7 on 2020-11-02 07:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clickcollect', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clickandcollect',
            name='reserve_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
