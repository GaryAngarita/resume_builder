from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
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

def experiencepage(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id)
        }
    return render(request, 'objandskill.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

# Create your views here.
