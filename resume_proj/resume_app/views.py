from django.contrib.messages.api import info
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, date
from time import strptime
import bcrypt
import imghdr
from .models import *

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def media(request):
    return render(request, "media.html")

def recommend(request):
    return render(request, "recommend.html")

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

def social(request):
    if request.method == 'GET':
        return redirect('/')    
    user = User.objects.get(id = request.session['id'])
    errors = Social.objects.site_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/personalinfo/{user.id}')
    mistakes = Contact.objects.address_validator(request.POST)
    if len(mistakes) > 0:
        for key, value in mistakes.items():
            messages.error(request, value)
        return redirect(f'/personalinfo/{user.id}')
    else:
        user = User.objects.get(id = request.session['id'])
        Contact.objects.create(street = request.POST['street'], 
        city = request.POST['city'], 
        state = request.POST['state'], 
        zip = request.POST['zip'], 
        phone_number = request.POST['phone_number'],
        user = user)
        Social.objects.create(github = request.POST['github'],
        linkedin = request.POST['linkedin'],
        facebook = request.POST['facebook'],
        twitter = request.POST['twitter'], 
        user = user)
        return redirect('/objectiveandskill')

def objectiveandskill(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id = request.session['id'])
        }
    return render(request, 'objandskill.html', context)

def objandskill(request):
    if request.method == 'GET':
        return redirect('/')
    mistakes = Objective.objects.obj_validator(request.POST)
    errors = Skill.objects.skill_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/objectiveandskill')
    if len(mistakes) > 0:
        for key, value in mistakes.items():
            messages.error(request, value)
        return redirect('/objectiveandskill')
    else:        
        user = User.objects.get(id = request.session['id'])
        Objective.objects.create(content = request.POST['content'], 
        user = user)
        Skill.objects.create(selected1 = request.POST['selected1'], 
        selected2 = request.POST['selected2'], 
        selected3 = request.POST['selected3'], 
        selected4 = request.POST['selected4'], 
        selected5 = request.POST['selected5'], 
        selected6 = request.POST['selected6'], 
        selected7 = request.POST['selected7'], 
        selected8 = request.POST['selected8'], 
        selected9 = request.POST['selected9'],
        user = user)
        return redirect('/experiencepage')

def experiencepage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id = request.session['id'])
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
        user = User.objects.get(id = request.session['id'])
        Experience.objects.create(title1 = request.POST['title1'], 
        desc1 = request.POST['desc1'],
        title2 = request.POST['title2'], 
        desc2 = request.POST['desc2'],
        title3 = request.POST['title3'], 
        desc3 = request.POST['desc3'], 
        user = user)
        return redirect('/employmentpage')

def employmentpage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id = request.session['id'])
        }
    return render(request, 'employment.html', context)

def employment(request):
    if request.method == 'GET':
        return redirect('/')
    errors = Employment.objects.emp_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/employmentpage')
    else:
        if request.POST['date_from1'] == '':
            date_from1 = None
        else:
            date_from1 = request.POST['date_from1']
        if request.POST['date_to1'] == '':
            date_to1 = None
        else:
            date_to1 = request.POST['date_to1']
        if request.POST['date_from2'] == '':
            date_from2 = None
        else:
            date_from2 = request.POST['date_from2']
        if request.POST['date_to2'] == '':
            date_to2 = None
        else:
            date_to2 = request.POST['date_to2']
        if request.POST['date_from3'] == '':
            date_from3 = None
        else:
            date_from3 = request.POST['date_from3']
        if request.POST['date_to3'] == '':
            date_to3 = None
        else:
            date_to3 = request.POST['date_to3']
        user = User.objects.get(id = request.session['id'])
        print(request.POST['date_from1'])
        Employment.objects.create(date_from1 = date_from1,
        date_to1 = date_to1, 
        title1 = request.POST['title1'], 
        desc1 = request.POST['desc1'],
        date_from2 = date_from2, 
        date_to2 = date_to2, 
        title2 = request.POST.get('title2', ''), 
        desc2 = request.POST.get('desc2', ''),
        date_from3 = date_from3, 
        date_to3 = date_to3, 
        title3 = request.POST.get('title3', ''), 
        desc3 = request.POST.get('desc3', ''), 
        user = user)
        return redirect('/educationpage')

def educationpage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id),
            'education': Education.objects.filter(user = user_id)
        }
    return render(request, 'education.html', context)

def education(request):
    if request.method == 'GET':
        return redirect('/')
    errors = Education.objects.edu_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/educationpage')
    else: 
        user = User.objects.get(id = request.session['id'])
        date_from = request.POST['date_from']
        if request.POST['date_from'] == '':
            date_from = None
        date_from1 = request.POST['date_from1']
        if request.POST['date_from1'] == '':
            date_from1 = None
        date_from2 = request.POST['date_from2']
        if request.POST['date_from2'] == '':
            date_from2 = None
        date_from3 = request.POST['date_from3']
        if request.POST['date_from3'] == '':
            date_from3 = None
        date_from4 = request.POST['date_from4']
        if request.POST['date_from4'] == '':
            date_from4 = None
        Education.objects.create(date_from = date_from,
        school = request.POST['school'], 
        program = request.POST['program'], 
        grad = request.POST['grad'], 
        date_from1 = date_from1,
        school1 = request.POST.get('school1'), 
        program1 = request.POST.get('program1'), 
        grad1 = request.POST.get('grad1'),
        date_from2 = date_from2,
        school2 = request.POST.get('school2'), 
        program2 = request.POST.get('program2'), 
        grad2 = request.POST.get('grad2'),
        date_from3 = date_from3,
        school3 = request.POST.get('school3'), 
        program3 = request.POST.get('program3'), 
        grad3 = request.POST.get('grad3'),
        date_from4 = date_from4,
        school4 = request.POST.get('school4'), 
        program4 = request.POST.get('program4'), 
        grad4 = request.POST.get('grad4'),
        user = user)
        return redirect('/additionalpage')

def additionalpage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id = request.session['id'])
        }
    return render(request, 'additional.html', context)

def additional(request):
    if request.method == 'GET':
        return redirect('/')
    errors = Additional.objects.add_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/additionalpage')    
    else:
        user = User.objects.get(id = request.session['id'])
        Additional.objects.create(info = request.POST.get('info'), 
        info1 = request.POST.get('info1'),
        info2 = request.POST.get('info2'),
        info3 = request.POST.get('info3'),
        info4 = request.POST.get('info4'),
        info5 = request.POST.get('info5'),
        info6 = request.POST.get('info6'),
        user = user)        
        return redirect('/picturepage')

def picturepage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id = request.session['id'])
        }
    return render(request, 'picture.html', context)

def picture(request):
    if request.method == 'GET':
        return redirect('/')
    # mistakes = Picture.objects.pic_validator(request.FILES)
    # if len(mistakes) > 0:
    #     for key, value in mistakes.items():
    #         messages.error(request, value)
    #     return redirect('/picturepage')
    else:
        img = (request.FILES, request.POST)
        user = User.objects.get(id = request.session['id'])
        if request.method == 'POST' and 'img' in request.FILES and request.FILES == '':
            Picture.objects.create(img = '', 
            user = user)
        elif request.method == 'POST' and 'img' in request.FILES and request.FILES != '':
            Picture.objects.create(img = img, 
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
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id = request.session['id'])
        }
    return render(request, 'preview.html', context)

def template1(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id)
        }
    return render(request, 'template1.html', context)

def template2(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id)
        }
    return render(request, 'template2.html', context)

def template3(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id)
        }
    return render(request, 'template3.html', context)

def template4(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['id']
        context = {
            'user': User.objects.get(id = user_id)
        }
    return render(request, 'template4.html', context)

def editpersonalpage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id = request.session['id'])
        }
    return render(request, 'editpersonal.html', context)

def editcontact(request):
    if request.method == 'GET':
        return redirect('/')
    mistakes = Social.objects.site_validator(request.POST)
    if len(mistakes) > 0:
        for key, value in mistakes.items():
            messages.error(request, value)
        return redirect(f'/editpersonalpage')
    errors = Contact.objects.address_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/editpersonalpage')
    frauds = User.objects.simp_validator(request.POST)
    if len(frauds) > 0:
        for key, value in frauds.items():
            messages.error(request, value)
        return redirect(f'/editpersonalpage')
    else:
        user = User.objects.get(id = request.session['id'])
        identity = User.objects.get(id = request.session['id'])
        identity.first_name = request.POST['first_name']
        identity.last_name = request.POST['last_name']
        identity.email = request.POST['email']
        identity.save()
        updated = Contact.objects.get(user = user)
        updated.street = request.POST['street']
        updated.city = request.POST['city']
        updated.state = request.POST['state']
        updated.zip = request.POST['zip']
        updated.phone_number = request.POST['phone_number']
        updated.save()
        new_soc = Social.objects.get(user = user)
        new_soc.github = request.POST.get('github', "")
        new_soc.linkedin = request.POST.get('linkedin', "")
        new_soc.facebook = request.POST.get('facebook', "")
        new_soc.twitter = request.POST.get('twitter', "")
        new_soc.save()
        return redirect(f'/resumehome/{user.id}')

def editobjandskillpage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id = request.session['id'])
        }
    return render(request, 'editobjandskill.html', context)

def editobjective(request):
    if request.method == 'GET':
        return redirect('/')
    mistakes = Skill.objects.skill_validator(request.POST)
    if len(mistakes) > 0:
        for key, value in mistakes.items():
            messages.error(request, value)
        return redirect(f'/editobjandskillpage')
    errors = Objective.objects.obj_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/editobjandskillpage')
    else:
        user = User.objects.get(id = request.session['id'])
        updated = Objective.objects.get(user = user)
        updated.content = request.POST['content']
        updated.save()
        new_skill = Skill.objects.get(user = user)
        new_skill.selected1 = request.POST['selected1']
        new_skill.selected2 = request.POST['selected2']
        new_skill.selected3 = request.POST['selected3']
        new_skill.selected4 = request.POST['selected4']
        new_skill.selected5 = request.POST['selected5']
        new_skill.selected6 = request.POST['selected6']
        new_skill.selected7 = request.POST['selected7']
        new_skill.selected8 = request.POST['selected8']
        new_skill.selected9 = request.POST['selected9']
        new_skill.save()
        return redirect(f'/resumehome/{user.id}')

def editexperiencepage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id = request.session['id'])
        }
    return render(request, 'editexperience.html', context)

def editexperience(request):
    if request.method == 'GET':
        return redirect('/')
    errors = Experience.objects.exp_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/editexperiencepage')
    else:
        user = User.objects.get(id = request.session['id'])
        updated = Experience.objects.get(user = user)
        updated.title1 = request.POST['title1']
        updated.desc1 = request.POST['desc1']
        updated.title2 = request.POST.get('title2', '')
        updated.desc2 = request.POST.get('desc2', '')
        updated.title3 = request.POST.get('title3', '')
        updated.desc3 = request.POST.get('desc3', '')
        updated.save()
        return redirect(f'/resumehome/{user.id}')

def editemploymentpage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'date': 'Y-m-d',
            'user': User.objects.get(id = request.session['id'])
        }
    return render(request, 'editemployment.html', context)

def editemployment(request):
    if request.method == 'GET':
        return redirect('/')
    errors = Employment.objects.emp_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/editemploymentpage')
    else:
        user = User.objects.get(id = request.session['id'])
        updated = Employment.objects.get(user = user)
        updated.date_from1 = request.POST['date_from1']
        updated.date_to1 = request.POST['date_to1']
        updated.title1 = request.POST['title1']
        updated.desc1 = request.POST['desc1']
        updated.date_from2 = request.POST.get('date_from2', None)
        updated.date_to2 = request.POST.get('date_to2', None)
        updated.title2 = request.POST.get('title2', '')
        updated.desc2 = request.POST.get('desc2', '')
        updated.date_from3 = request.POST.get('date_from3', None)
        updated.date_to3 = request.POST.get('date_to3', None)
        updated.title3 = request.POST.get('title3', '')
        updated.desc3 = request.POST.get('desc3', '')
        updated.save()
        return redirect(f'/resumehome/{user.id}')

def editeducationpage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'date': 'Y-m-d',
            'user': User.objects.get(id = request.session['id'])
        }
    return render(request, 'editeducation.html', context)

def editeducation(request):
    if request.method == 'GET':
        return redirect('/')
    errors = Education.objects.edu_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/editeducationpage')
    else:
        user = User.objects.get(id = request.session['id'])
        updated = Education.objects.get(user = user)
        date_from = request.POST['date_from']
        if request.POST['date_from'] == '':
            date_from = None
        date_from1 = request.POST['date_from1']
        if request.POST['date_from1'] == '':
            date_from1 = None
        date_from2 = request.POST['date_from2']
        if request.POST['date_from2'] == '':
            date_from2 = None
        date_from3 = request.POST['date_from3']
        if request.POST['date_from3'] == '':
            date_from3 = None
        date_from4 = request.POST['date_from4']
        if request.POST['date_from4'] == '':
            date_from4 = None
        updated.date_from = date_from
        updated.school = request.POST['school']
        updated.program = request.POST['program']
        updated.grad = request.POST['grad']
        updated.date_from1 = date_from1
        updated.school1 = request.POST.get('school1', '')
        updated.program1 = request.POST.get('program1', '')
        updated.grad1 = request.POST.get('grad1', None)
        updated.date_from2 = date_from2
        updated.school2 = request.POST.get('school2', '')
        updated.program2 = request.POST.get('program2', '')
        updated.grad2 = request.POST.get('grad2', None)
        updated.date_from3 = date_from3
        updated.school3 = request.POST.get('school3', '')
        updated.program3 = request.POST.get('program3', '')
        updated.grad3 = request.POST.get('grad3', None)
        updated.date_from4 = date_from4
        updated.school4 = request.POST.get('school4', '')
        updated.program4 = request.POST.get('program4', '')
        updated.grad4 = request.POST.get('grad4', None)
        updated.save()
        return redirect(f'/resumehome/{user.id}')

def editadditionalpage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id = request.session['id'])
        }
    return render(request, 'editadditional.html', context)

def editadditional(request):
    if request.method == 'GET':
        return redirect('/')
    errors = Additional.objects.add_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/editadditionalpage')
    else:
        user = User.objects.get(id = request.session['id'])
        updated = Additional.objects.get(user = user)
        updated.info = request.POST.get('info', '')
        updated.info1 = request.POST.get('info1', '')
        updated.info2 = request.POST.get('info2', '')
        updated.info3 = request.POST.get('info3', '')
        updated.info4 = request.POST.get('info4', '')
        updated.info5 = request.POST.get('info5', '')
        updated.info6 = request.POST.get('info6', '')
        updated.save()
        return redirect(f'/resumehome/{user.id}')

def editpicturepage(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id = request.session['id'])
        }
    return render(request, 'editpicture.html', context)

def editpicture(request):
    if request.method == 'GET':
        return redirect('/')
    # errors = Picture.objects.pic_validator(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value)
        # return redirect('/editpicturepage')
    else:
        user = User.objects.get(id = request.session['id'])
        updated = Picture.objects.get(user = user)
        updated.img = request.FILES['img']
        updated.save()
        return redirect(f'/resumehome/{user.id}')

def logout(request):
    request.session.flush()
    return redirect('/')

# Create your views here.
