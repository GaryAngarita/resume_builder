# Generated by Django 2.2 on 2021-07-20 22:10

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='date_from1',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today, message='Date must be in the past')]),
        ),
        migrations.AlterField(
            model_name='education',
            name='date_from2',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today, message='Date must be in the past')]),
        ),
        migrations.AlterField(
            model_name='education',
            name='date_from3',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today, message='Date must be in the past')]),
        ),
        migrations.AlterField(
            model_name='education',
            name='date_from4',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today, message='Date must be in the past')]),
        ),
    ]
