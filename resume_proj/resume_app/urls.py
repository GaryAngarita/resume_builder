from django.urls import path
from . import views

urlpatterns = [
    path('', views.logreg),
    path('register', views.register),
    path('login', views.login),
    path('newresume/<int:user_id>', views.newresume),
    path('resumehome/<int:user_id>', views.resumehome),
    path('personalinfo/<int:user_id>', views.personalinfo),
    path('contact', views.contact),
    path('social', views.social),
    path('objectiveandskill', views.objectiveandskill),
    path('objective', views.objective),
    path('skill', views.skill),
    path('experiencepage', views.experiencepage),
    path('experience', views.experience),
    path('employmentpage', views.employmentpage),
    path('employment', views.employment),
    path('educationpage', views.educationpage),
    path('education', views.education),
    path('additionalpage', views.additionalpage),
    path('additional', views.additional),
    path('picture', views.picture),
    path('logout', views.logout),
]