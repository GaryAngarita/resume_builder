from django.contrib.messages.api import info
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

# def contact(request):
#     if request.method == 'GET':
#         return redirect('/')
    
#     else:        
#         user_id = request.session['id']
#         user = User.objects.get(id = user_id)
        
#         return redirect(f'/personalinfo/{user.id}')

def social(request):
    if request.method == 'GET':
        return redirect('/')    
    user = User.objects.get(id = request.session['id'])
    mistakes = Contact.objects.address_validator(request.POST)
    if len(mistakes) > 0:
        for key, value in mistakes.items():
            messages.error(request, value)
        return redirect(f'/personalinfo/{user.id}')
    errors = Social.objects.site_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/personalinfo/{user.id}')
    else:        
        user_id = request.session['id']
        user = User.objects.get(id = user_id)
        Contact.objects.create(street = request.POST['street'], 
        city = request.POST['city'], 
        state = request.POST['state'], 
        zip = request.POST['zip'], 
        phone_number = request.POST['phone_number'],
        user = user)
        Social.objects.create(site = request.POST.getlist('site'), 
        user = user)
        return redirect('/objectiveandskill')

def objectiveandskill(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id)
        }
    return render(request, 'objandskill.html', context)

# def objective(request):
#     if request.method == 'GET':
#         return redirect('/')
#     errors = Objective.objects.obj_validator(request.POST)
#     if len(errors) > 0:
#         for key, value in errors.items():
#             messages.error(request, value)
#         return redirect('/')
#     else:        
#         user_id = request.session['id']
#         user = User.objects.get(id = user_id)
        
#         return redirect('/experiencepage')

def objandskill(request):
    if request.method == 'GET':
        return redirect('/')
    user = User.objects.get(id = request.session['id'])
    mistakes = Objective.objects.obj_validator(request.POST)
    if len(mistakes) > 0:
        for key, value in mistakes.items():
            messages.error(request, value)
        return redirect(f'/objective/{user.id}')
    errors = Skill.objects.skill_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/objective/{user.id}')
    else:        
        user_id = request.session['id']
        user = User.objects.get(id = user_id)
        Objective.objects.create(content = request.POST['content'], 
        user = user)
        Skill.objects.create(selected = request.POST.getlist('selected'), 
        user = user)
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
    errors = Experience.objects.exp_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/experiencepage')
    else:        
        user_id = request.session['id']
        user = User.objects.get(id = user_id)
        Experience.objects.create(title = request.POST.getlist('title'), 
        desc = request.POST.getlist('desc'), 
        user = user)
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
    errors = Employment.objects.emp_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:        
        user_id = request.session['id']
        user = User.objects.get(id = user_id)
        Employment.objects.create(date_from = request.POST.getlist('date_from'), 
        date_to = request.POST.getlist('date_to'), 
        title = request.POST.getlist('title'), 
        desc = request.POST.getlist('desc'), 
        user = user)
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
    errors = Education.objects.edu_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:        
        user_id = request.session['id']
        user = User.objects.get(id = user_id)
        Education.objects.create(date_from = request.POST.getlist('date_from'), 
        date_to = request.POST.getlist('date_to'), 
        school = request.POST.getlist('school'), 
        program = request.POST.getlist('program'), 
        grad = request.POST.getlist('grad'), 
        user = user)
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
    errors = Additional.objects.add_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:        
        user_id = request.session['id']
        user = User.objects.get(id = user_id)
        Additional.objects.create(info = request.POST.getlist('info'), 
        user = user)
        return redirect('/templatepage')

def picture(request):
    if request.method == 'GET':
        return redirect('/')
    errors = Picture.objects.pic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:        
        user_id = request.session['id']
        user = User.objects.get(id = user_id)
        Picture.objects.create(img = request.POST['img'], 
        user = user)
        return redirect('/templatepage')

# def picture(request):
#     if request.method == 'POST':
#         uploaded_file = request.FILES['img']
#         fs = FileSystemStorage()
#         fs.save(uploaded_file.name, uploaded_file.size)
#         print(uploaded_file.name)
#         print(uploaded_file.size)
#     return redirect('/templatepage')

def templatepage(request):
    return render(request, 'preview.html')

def editpersonalpage(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id),
            'contact': Contact.objects.get(id = user_id),
            'social': Social.objects.get(id = user_id)
        }
    return render(request, 'editpersonal.html', context)

def editcontact(request, user_id):
    if request.method == 'GET':
        return redirect('/')
    errors = Contact.objects.address_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(id = user_id)
        updated = Contact.objects.get(id = user)
        updated.street = request.POST['street']
        updated.city = request.POST['city']
        updated.state = request.POST['state']
        updated.zip = request.POST['zip']
        updated.phone_number = request.POST['phone_number']
        updated.save()
        request.session['id'] = user.id
        return redirect(f'/resumehome/{user.id}')

def editsocial(request, user_id):
    if request.method == 'GET':
        return redirect('/')
    errors = Social.objects.site_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(id = user_id)
        updated = Social.objects.get(id = user)
        updated.site = request.POST.getlist('site')
        updated.save()
        request.session['id'] = user.id
        return redirect(f'/resumehome/{user.id}')

def editobjandskillpage(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id),
            'objective': Objective.objects.get(id = user_id),
            'skill': Skill.objects.get(id = user_id)
        }
    return render(request, 'editobjandskill.html', context)

def editobjective(request, user_id):
    if request.method == 'GET':
        return redirect('/')
    errors = Objective.objects.obj_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(id = user_id)
        updated = Objective.objects.get(id = user)
        updated.content = request.POST['content']
        updated.save()
        request.session['id'] = user.id
        return redirect(f'/resumehome/{user.id}')

def editskill(request, user_id):
    if request.method == 'GET':
        return redirect('/')
    errors = Skill.objects.skill_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(id = user_id)
        updated = Skill.objects.get(id = user)
        updated.selected = request.POST.getlist('selected')
        updated.save()
        request.session['id'] = user.id
        return redirect(f'/resumehome/{user.id}')

def editexperiencepage(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id),
            'experience': Experience.objects.get(id = user_id)
        }
    return render(request, 'editexperience.html', context)

def editexperience(request, user_id):
    if request.method == 'GET':
        return redirect('/')
    errors = Experience.objects.exp_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(id = user_id)
        updated = Experience.objects.get(id = user)
        updated.title = request.POST.getlist('title')
        updated.desc = request.POST.getlist('desc')
        updated.save()
        request.session['id'] = user.id
        return redirect(f'/resumehome/{user.id}')

def editemploymentpage(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id),
            'employment': Employment.objects.get(id = user_id)
        }
    return render(request, 'editemployment.html', context)

def editemployment(request, user_id):
    if request.method == 'GET':
        return redirect('/')
    errors = Employment.objects.emp_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(id = user_id)
        updated = Employment.objects.get(id = user)
        updated.date_from = request.POST.getlist('date_from')
        updated.date_to = request.POST.getlist('date_to')
        updated.title = request.POST.getlist('title')
        updated.desc = request.POST.getlist('desc')
        updated.save()
        request.session['id'] = user.id
        return redirect(f'/resumehome/{user.id}')

def editeducationpage(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id),
            'education': Education.objects.get(id = user_id)
        }
    return render(request, 'editeducation.html', context)

def editeducation(request, user_id):
    if request.method == 'GET':
        return redirect('/')
    errors = Education.objects.edu_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(id = user_id)
        updated = Education.objects.get(id = user)
        updated.date_from = request.POST.getlist('date_from')
        updated.date_to = request.POST.getlist('date_to')
        updated.school = request.POST.getlist('school')
        updated.program = request.POST.getlist('program')
        updated.grad = request.POST.getlist('grad')
        updated.save()
        request.session['id'] = user.id
        return redirect(f'/resumehome/{user.id}')

def editadditionalpage(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id),
            'additional': Additional.objects.get(id = user_id)
        }
    return render(request, 'editadditional.html', context)

def editadditional(request, user_id):
    if request.method == 'GET':
        return redirect('/')
    errors = Additional.objects.add_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(id = user_id)
        updated = Additional.objects.get(id = user)
        updated.info = request.POST.getlist('info')
        updated.save()
        request.session['id'] = user.id
        return redirect(f'/resumehome/{user.id}')

def editpicture(request, user_id):
    if request.method == 'GET':
        return redirect('/')
    errors = Picture.objects.pic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(id = user_id)
        updated = Picture.objects.get(id = user)
        updated.img = request.POST['img']
        updated.save()
        request.session['id'] = user.id
        return redirect(f'/resumehome/{user.id}')


def logout(request):
    request.session.flush()
    return redirect('/')

# Create your views here.
