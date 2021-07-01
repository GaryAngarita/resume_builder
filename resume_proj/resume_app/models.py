from django.contrib.messages.api import error
from django.db import models
import re
from localflavor.models import USStateField
from django.db.models.fields import DateTimeField
from django.core.validators import RegexValidator
import bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        user_emails = User.objects.filter(email = postData['email'])
        if len(postData['first_name']) == 0:
            errors['blank_first'] = "First name cannot be blank"
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be 2 letters or more"
        if len(postData['last_name']) == 0:
            errors['blank_last'] = 'Last name cannot be blank'
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be 2 letters or more"
        if len(postData['email']) == 0:
            errors['blank_email'] = "Email cannot be blank"
        if not email_regex.match(postData['email']):
            errors['email'] = "Not a valid email address"
        if user_emails:
            errors['user_email'] = "Email already in use"
        if len(postData['password']) == 0:
            errors['blank_password'] = "Password is required"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be 8 characters or more"
        if postData['password'] != postData['pw_conf']:
            errors['confirm'] = "Passwords do not match"
        return errors

    def log_validator(self, postData):
        errors = {}
        user_emails = User.objects.filter(email = postData['email'])
        if not email_regex.match(postData['email']):
            errors['email'] = "Invalid email address"
        if not user_emails:
            errors['mismatch'] = "Email does not exist"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if bcrypt.checkpw(postData['password'].encode(), user_emails[0].password.encode()):
            print("password match")
        else:
            errors['bad_password'] = "Email and password do not match"
        return errors
        

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = UserManager()

class ContactManager(models.Manager):
    def address_validator(self, postData):
        errors = {}
        if len(postData['street']) < 2:
            errors['street'] = "Enter a legit street"
        #insert phone validation error here
        return errors

class Contact(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = ContactManager()

class Social(models.Model):
    site = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="social_medias", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    #objects = SocialManager()

class Objective(models.Model):
    content = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    #objects = ObjectiveManager()

class Skill(models.Model):
    selected = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="skills", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    #objects = SkillManager()

class Experience(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    user = models.ForeignKey(User, related_name="experiences", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    #objects = ExperienceManager()

class Employment(models.Model):
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    title = models.CharField(max_length=100)
    desc = models.TextField()
    user = models.ForeignKey(User, related_name="employments", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    #objects = EmploymentManager()

class Education(models.Model):
    GRAD_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    school = models.CharField(max_length=255)
    program = models.CharField(max_length=255)
    grad = models.CharField(max_length=1, choices=GRAD_CHOICES, default='Y')
    user = models.ForeignKey(User, related_name="educations", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    #objects = EducationManager()

class Additional(models.Model):
    info = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="additionals", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    #objects = AdditionalManager()

class Picture(models.Model):
    img = models.ImageField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    #objects = PictureManager()

# Create your models here.
