# Generated by Django 3.0.7 on 2021-01-19 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0003_auto_20200216_0346'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='survey',
            name='slug',
            field=models.SlugField(default='municipales-2020'),
            preserve_default=False,
        ),
    ]