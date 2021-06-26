from django.urls import path
from . import views

urlpatterns = [
    path('', views.logreg),
    path('register', views.register),
    path('login', views.login),
    path('newresume', views.newresume),
    path('resumehome', views.resumehome),
    path('logout', views.logout),
]