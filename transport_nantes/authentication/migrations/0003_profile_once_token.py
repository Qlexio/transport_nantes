# Generated by Django 3.0.7 on 2021-01-31 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20201121_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='once_token',
            field=models.BooleanField(default=False),
        ),
    ]