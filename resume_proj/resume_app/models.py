from django.contrib.messages.api import error
from django.db import models
import re
from django.db.models.fields import DateTimeField
from django.core.validators import RegexValidator, URLValidator, validate_image_file_extension
from django.db.models.fields.files import ImageField
import bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
phone_regex = RegexValidator(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', 'Valid phone number is required')

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
        if not phone_regex(postData['phone_number']):
            errors['phone_number'] = "You must enter a valid phone number"
        if len(postData['zip']) < 5 or len(postData['zip']) > 5:
            errors['zip'] = "Zip code must be 5 numbers"
        if len(postData['phone_number']) < 10:
            errors['short_number'] = "Phone number must be 10 digits"
        return errors

class Contact(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = ContactManager()

class SocialManager(models.Manager):
    def site_validator(self, postData):
        errors = {}
        if URLValidator(postData['site']) == True:
            print('Site is valid')
        else:
            errors['site'] = 'Check your website and try again'
        
        return errors

class Social(models.Model):
    site = models.URLField(max_length=200)
    user = models.ForeignKey(User, related_name="social_medias", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = SocialManager()

class ObjectiveManager(models.Manager):
    def obj_validator(self, postData):
        errors = {}
        if len(postData['content']) < 25:
            errors['content'] = "You should expand on your Objective more"
        return errors

class Objective(models.Model):
    content = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = ObjectiveManager()

class SkillManager(models.Manager):
    def skill_validator(self, postData):
        errors = {}
        if postData['selected'] != '' and len(postData['selected']) < 5:
            errors['selected'] = "Skill should be longer than 5 characters"
        if postData['selected'] < 6:
            errors['few_selected'] = "You should have at least 6 Skills"
        return errors

class Skill(models.Model):
    selected = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="skills", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = SkillManager()

class ExperienceManager(models.Manager):
    def exp_validator(self, postData):
        errors = {}
        if postData['title'] != '' and len(postData['title']) < 2:
            errors['title'] = "Title should be expanded"
        if postData['desc'] != '' and len(postData['desc']) < 10:
            errors['desc'] = "Experience description should be expanded"
        return errors

class Experience(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    user = models.ForeignKey(User, related_name="experiences", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = ExperienceManager()

class EmploymentManager(models.Manager):
    def emp_validator(self, postData):
        errors = {}
        #need to figure out how to deal with date
        if postData['date_from'] == 'Today':
            errors['date_from'] = "Date must be in the past"
        if postData['title'] != '' and len(postData['title']) < 2:
            errors['title'] = "Title should be expanded"
        if postData['desc'] != '' and len(postData['desc']) < 10:
            errors['desc'] = "Employment description should be expanded"
        return errors

class Employment(models.Model):
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    title = models.CharField(max_length=100)
    desc = models.TextField()
    user = models.ForeignKey(User, related_name="employments", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = EmploymentManager()

class EducationManager(models.Manager):
    def edu_validator(self, postData):
        errors = {}
        #need to figure out how to deal with date
        if postData['date_from'] == 'Today':
            errors['date_from'] = "Date must be in the past"
        if postData['school'] != '' and len(postData['school']) < 5:
            errors['school'] = "Schools need to be spelled out"
        if postData['program'] != '' and len(postData['program']) < 5:
            errors['program'] = "Program needs to be spelled out"
        return errors

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
    objects = EducationManager()

class AdditionalManager(models.Manager):
    def add_validator(self, postData):
        errors = {}
        if postData['info'] != '' and len(postData['info']) < 5:
            errors['info'] = "You should expand on your shorter entry"
        return errors

class Additional(models.Model):
    info = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="additionals", on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = AdditionalManager()

# class PictureManager(models.Manager):
#     def pic_validator(self, postData):
#         errors = {}
#         if postData['img'] != '' and postData['img'] not validate_image_file_extension

class Picture(models.Model):
    img = models.ImageField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    #objects = PictureManager()

# Create your models here.
