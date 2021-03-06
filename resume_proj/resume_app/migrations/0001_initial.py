# Generated by Django 2.2 on 2021-07-27 22:06

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github', models.CharField(blank=True, max_length=200)),
                ('linkedin', models.CharField(blank=True, max_length=200)),
                ('facebook', models.CharField(blank=True, max_length=200)),
                ('twitter', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_medias', to='resume_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected1', models.CharField(blank=True, max_length=255)),
                ('selected2', models.CharField(blank=True, max_length=255)),
                ('selected3', models.CharField(blank=True, max_length=255)),
                ('selected4', models.CharField(blank=True, max_length=255)),
                ('selected5', models.CharField(blank=True, max_length=255)),
                ('selected6', models.CharField(blank=True, max_length=255)),
                ('selected7', models.CharField(blank=True, max_length=255)),
                ('selected8', models.CharField(blank=True, max_length=255)),
                ('selected9', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='resume_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='resume_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='resume_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title1', models.CharField(blank=True, max_length=100)),
                ('desc1', models.TextField(blank=True)),
                ('title2', models.CharField(blank=True, max_length=100)),
                ('desc2', models.TextField(blank=True)),
                ('title3', models.CharField(blank=True, max_length=100)),
                ('desc3', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='resume_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from1', models.DateField(blank=True)),
                ('date_to1', models.DateField(null=True)),
                ('title1', models.CharField(blank=True, max_length=100)),
                ('desc1', models.TextField(blank=True)),
                ('date_from2', models.DateField(blank=True, null=True)),
                ('date_to2', models.DateField(blank=True, null=True)),
                ('title2', models.CharField(blank=True, max_length=100)),
                ('desc2', models.TextField(blank=True)),
                ('date_from3', models.DateField(blank=True, null=True)),
                ('date_to3', models.DateField(blank=True, null=True)),
                ('title3', models.CharField(blank=True, max_length=100)),
                ('desc3', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employments', to='resume_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(blank=True)),
                ('school', models.CharField(max_length=255)),
                ('program', models.CharField(max_length=255)),
                ('grad', models.CharField(max_length=1)),
                ('date_from1', models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today, message='Date must be in the past')])),
                ('school1', models.CharField(max_length=255)),
                ('program1', models.CharField(max_length=255)),
                ('grad1', models.CharField(max_length=1)),
                ('date_from2', models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today, message='Date must be in the past')])),
                ('school2', models.CharField(max_length=255)),
                ('program2', models.CharField(max_length=255)),
                ('grad2', models.CharField(max_length=1)),
                ('date_from3', models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today, message='Date must be in the past')])),
                ('school3', models.CharField(blank=True, max_length=255, null=True)),
                ('program3', models.CharField(max_length=255)),
                ('grad3', models.CharField(blank=True, max_length=1, null=True)),
                ('date_from4', models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today, message='Date must be in the past')])),
                ('school4', models.CharField(blank=True, max_length=255)),
                ('program4', models.CharField(max_length=255)),
                ('grad4', models.CharField(blank=True, max_length=1, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to='resume_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=2)),
                ('zip', models.CharField(max_length=5)),
                ('phone_number', models.CharField(blank=True, max_length=17)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='resume_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Additional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(max_length=255)),
                ('info1', models.CharField(blank=True, max_length=255)),
                ('info2', models.CharField(blank=True, max_length=255)),
                ('info3', models.CharField(blank=True, max_length=255)),
                ('info4', models.CharField(blank=True, max_length=255)),
                ('info5', models.CharField(blank=True, max_length=255)),
                ('info6', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additionals', to='resume_app.User')),
            ],
        ),
    ]
