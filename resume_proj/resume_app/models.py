from django.contrib.messages.api import error
from django.db import models
import re
from datetime import date

from django.utils import timezone
from django.db.models.fields import DateTimeField
from django.core.validators import RegexValidator, URLValidator, validate_image_file_extension, MaxValueValidator
from django.db.models.fields.files import ImageField
import bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

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
        if user_emails and postData['email'] != postData['email']:
            errors['user_email'] = "Email already in use"
        if not email_regex.match(postData['email']):
            errors['email'] = "Invalid email address"
        if len(postData['street']) < 2:
            errors['street'] = "Enter a legit street"
        if len(postData['zip']) != 5:
            errors['zip'] = "Zip code must be 5 numbers"
        if len(postData['phone_number']) < 10:
            errors['short_number'] = "Phone number must be 10 digits"

        return errors

class Contact(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=17, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = ContactManager()

class SocialManager(models.Manager):
    def site_validator(self, postData):
        errors = {}
        if len(postData['github']) < 4:
            errors['github'] = "Check your GitHub site again"
        if len(postData['linkedin']) < 4:
            errors['linkedin'] = "Check your LinkedIn site again"
        if len(postData['facebook']) < 4:
            errors['facebook'] = "Check your Facebook site again"
        if len(postData['twitter']) < 4:
            errors['twitter'] = "Check your Twitter site again"
        # if postData['site'] != '':
        #     if not url_regex.match(postData['site']):
        #         errors['site'] = 'Check your website and try again'
        #     else:
        #         print('Site is valid')
        return errors

class Social(models.Model):
    github = models.CharField(max_length=200, blank=True)
    linkedin = models.CharField(max_length=200, blank=True)
    facebook = models.CharField(max_length=200, blank=True)
    twitter = models.CharField(max_length=200, blank=True)
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
        if len(postData['selected1']) < 1:
            errors['few_selected1'] = "You should have 9 Skills"
        if len(postData['selected2']) < 1:
            errors['few_selected2'] = "You should have 9 Skills"
        if len(postData['selected3']) < 1:
            errors['few_selected3'] = "You should have 9 Skills"
        if len(postData['selected4']) < 1:
            errors['few_selected4'] = "You should have 9 Skills"
        if len(postData['selected5']) < 1:
            errors['few_selected5'] = "You should have 9 Skills"
        if len(postData['selected6']) < 1:
            errors['few_selected6'] = "You should have 9 Skills"
        if len(postData['selected7']) < 1:
            errors['few_selected7'] = "You should have 9 Skills"
        if len(postData['selected8']) < 1:
            errors['few_selected8'] = "You should have 9 Skills"
        if len(postData['selected9']) < 1:
            errors['few_selected9'] = "You should have 9 Skills"
        return errors

class Skill(models.Model):
    selected1 = models.CharField(max_length=255, blank=True)
    selected2 = models.CharField(max_length=255, blank=True)
    selected3 = models.CharField(max_length=255, blank=True)
    selected4 = models.CharField(max_length=255, blank=True)
    selected5 = models.CharField(max_length=255, blank=True)
    selected6 = models.CharField(max_length=255, blank=True)
    selected7 = models.CharField(max_length=255, blank=True)
    selected8 = models.CharField(max_length=255, blank=True)
    selected9 = models.CharField(max_length=255, blank=True)
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
        # if postData['date_from'] >= timezone.now().date():
        #     errors['date_from'] = "Date must be in the past"
        if postData['title'] != '' and len(postData['title']) < 2:
            errors['title'] = "Title should be expanded"
        if postData['desc'] != '' and len(postData['desc']) < 10:
            errors['desc'] = "Employment description should be expanded"
        return errors

class Employment(models.Model):
    date_from = models.DateField(validators=[MaxValueValidator(limit_value=date.today, message="Date must be in the past")])
    date_to = models.DateField(blank=True)
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
        if postData['school'] != '' and len(postData['school']) < 2:
            errors['school'] = "Schools need to be spelled out"
        if postData['program'] != '' and len(postData['program']) < 5:
            errors['program'] = "Program needs to be spelled out"
        return errors

class Education(models.Model):
    date_from = models.DateField(validators=[MaxValueValidator(limit_value=date.today, message="Date must be in the past")])
    school = models.CharField(max_length=255)
    program = models.CharField(max_length=255)
    grad = models.CharField(max_length=1)
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
#     def pic_validator(self, postFile):
#         image_regex = "([^\\s]+(\\.(?i)(jpe?g|png|gif|bmp))$)"
#         errors = {}
#         test = re.compile(image_regex)
#         # if (postFile['img'] == None):
#         #     return False
#         if (re.search(test, str(postFile['img']))) == False:
#             # print(imghdr.what(postFile['img']))
#             # return True
#         # else:
#             errors['img'] = "That is not a supported image type. Must be .jpg, .png, .gif, .bmp"
#         return errors
        # elif postData['img'] != '' and len(postData['img']) < 4:
        #     errors['not_img'] = "Filename must be greater than 4 characters"

class Picture(models.Model):
    img = models.ImageField(upload_to='images/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    # objects = PictureManager()

# Create your models here.
