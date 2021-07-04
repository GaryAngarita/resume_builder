from django.contrib.messages.api import info
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from django.core.files.storage import FileSystemStorage
from .models import *

def logreg(request):
    return render(request, 'logreg.html')

def register(request):
    errors = User.objects.reg_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        user = User.objects.create(first_name= request.POST['first_name'], 
        last_name= request.POST['last_name'], 
        email= request.POST['email'], 
        password=pw_hash)
        messages.success(request, "Registration successful!")
        request.session['id'] = user.id
        return redirect(f'/newresume/{user.id}')

def login(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.log_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['id'] = user.id
        return redirect(f'/resumehome/{user.id}')

def newresume(request, user_id):
    context = {
            'user': User.objects.get(id = user_id)
        }
    return render(request, "postregister.html", context)

def resumehome(request, user_id):
    context = {
            'user': User.objects.get(id = user_id)
        }
    return render(request, "postlogin.html", context)

def personalinfo(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id = user_id)
        }
        return render(request, 'personalinfo.html', context)

def contact(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.address_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_id = request.session['id']
        Social.objects.create(street = request.POST['street'], 
        city = request.POST['street'], 
        state = request.POST['state'], 
        zip = request.POST['zip'], 
        phone_number = request.POST['site'],
        user = user_id)
        return redirect('/objectiveandskill')

def social(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.site_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_id = request.session['id']
        Social.objects.create(site = request.POST['site'], 
        user = user_id)
        return redirect('/objectiveandskill')

def objectiveandskill(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id)
        }
    return render(request, 'objandskill.html', context)

def objective(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.obj_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_id = request.session['id']
        Objective.objects.create(content = request.POST['content'], 
        user = user_id)
        return redirect('/experiencepage')

def skill(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.skill_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_id = request.session['id']
        Skill.objects.create(selected = request.POST['selected'], 
        user = user_id)
        return redirect('/experiencepage')

def experiencepage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id)
        }
    return render(request, 'experience.html', context)

def experience(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.exp_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_id = request.session['id']
        Experience.objects.create(title = request.POST['title'], 
        desc = request.POST['desc'], 
        user = user_id)
        return redirect('/employmentpage')

def employmentpage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id)
        }
    return render(request, 'employment.html', context)

def employment(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.emp_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_id = request.session['id']
        Employment.objects.create(date_from = request.POST['date_from'], 
        date_to = request.POST['date_to'], 
        title = request.POST['title'], 
        desc = request.POST['desc'], 
        user = user_id)
        return redirect('/educationpage')

def educationpage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id)
        }
    return render(request, 'education.html', context)

def education(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.edu_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_id = request.session['id']
        Education.objects.create(date_from = request.POST['date_from'], 
        date_to = request.POST['date_to'], 
        school = request.POST['school'], 
        program = request.POST['program'], 
        grad = request.POST['grad'], 
        user = user_id)
        return redirect('/additionalpage')

def additionalpage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id)
        }
    return render(request, 'additional.html', context)

def additional(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.add_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_id = request.session['id']
        Additional.objects.create(info = request.POST['info'], 
        user = user_id)
        return redirect('/templatepage')

# def picture(request):
#     if request.method == 'GET':
#         return redirect('/')
#     errors = User.objects.add_validator(request.POST)
#     if len(errors) > 0:
#         for key, value in errors.items():
#             messages.error(request, value)
#         return redirect('/')
#     else:
#         user_id = request.session['id']
#         Additional.objects.create(img = request.POST['img'], 
#         user = user_id)
#         return redirect('/templatepage')

def picture(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['img']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file.size)
        print(uploaded_file.name)
        print(uploaded_file.size)
    return render(request, 'additional.html')

def logout(request):
    request.session.flush()
    return redirect('/')

# Create your views here.
