# Generated by Django 2.2 on 2021-07-14 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_app', '0005_auto_20210712_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='grad',
            field=models.CharField(max_length=1),
        ),
    ]