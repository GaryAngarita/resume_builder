from django.shortcuts import render, redirect

def logreg(request):
    return render(request, 'personalinfo.html')

def register(request):
    pass

def login(request):
    pass

def newresume(request):
    pass

def resumehome(request):
    pass

def logout(request):
    request.session.flush()
    return redirect('/')

# Create your views here.
