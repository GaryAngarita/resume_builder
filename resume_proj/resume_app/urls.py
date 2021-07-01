from django.urls import path
from . import views

urlpatterns = [
    path('', views.logreg),
    path('register', views.register),
    path('login', views.login),
    path('newresume/<int:user_id>', views.newresume),
    path('resumehome/<int:user_id>', views.resumehome),
    path('personalinfo/<int:user_id>', views.personalinfo),
    path('logout', views.logout),
]