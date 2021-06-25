from django.db import models
import re

from django.db.models.fields import DateTimeField
import bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = UserManager()

class Contact(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip = models.IntegerField(max_length=5)
    phone = models.IntegerField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = ContactManager()

class Social(models.Model):
    site = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="social_medias", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = SocialManager()

class Objective(models.Model):
    content = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = ObjectiveManager()

class Skill(models.Model):
    selected = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="skills", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = SkillManager()

class Experience(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    user = models.ForeignKey(User, related_name="experiences", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = ExperienceManager()

class Employment(models.Model):
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    title = models.CharField(max_length=100)
    desc = models.TextField()
    user = models.ForeignKey(User, related_name="employments", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = EmploymentManager()

class Education(models.Model):
    CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    school = models.CharField(max_length=255)
    program = models.CharField(max_length=255)
    grad = models.CharField(max_length=1, choices=CHOICES, default='Y')
    user = models.ForeignKey(User, related_name="educations", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = EducationManager()

class Additional(models.Model):
    info = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="additionals", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = AdditionalManager()

class Picture(models.Model):
    img = models.ImageField()

# Create your models here.
