# Generated by Django 2.2 on 2021-07-15 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume_app', '0010_auto_20210715_1426'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='date_to',
        ),
    ]