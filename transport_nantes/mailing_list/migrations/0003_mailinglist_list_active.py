# Generated by Django 3.0.7 on 2020-12-05 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_list', '0002_auto_20201121_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailinglist',
            name='list_active',
            field=models.BooleanField(default=False),
        ),
    ]
