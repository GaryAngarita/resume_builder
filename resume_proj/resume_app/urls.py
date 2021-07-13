from django.urls import path
from . import views

urlpatterns = [
    path('', views.logreg),
    path('register', views.register),
    path('login', views.login),
    path('newresume/<int:user_id>', views.newresume),
    path('resumehome/<int:user_id>', views.resumehome),
    path('personalinfo/<int:user_id>', views.personalinfo),
    #path('contact', views.contact),
    path('social', views.social),
    path('objectiveandskill', views.objectiveandskill),
    # path('objective', views.objective),
    path('objandskill', views.objandskill),
    path('experiencepage', views.experiencepage),
    path('experience', views.experience),
    path('employmentpage', views.employmentpage),
    path('employment', views.employment),
    path('educationpage', views.educationpage),
    path('education', views.education),
    path('additionalpage', views.additionalpage),
    path('additional', views.additional),
    # path('picture/', views.picture),
    path('templatepage', views.templatepage),
    path('editpersonalpage/<int:user_id>', views.editpersonalpage),
    path('editcontact/<int:user_id>', views.editcontact),
    path('editsocial/<int:user_id>', views.editsocial),
    path('editobjandskillpage/<int:user_id>', views.editobjandskillpage),
    path('editobjective/<int:user_id>', views.editobjective),
    path('editskill/<int:user_id>', views.editskill),
    path('editexperiencepage/<int:user_id>', views.editexperiencepage),
    path('editexperience/<int:user_id>', views.editexperience),
    path('editemploymentpage/<int:user_id>', views.editemploymentpage),
    path('editemployment/<int:user_id>', views.editemployment),
    path('editeducationpage/<int:user_id>', views.editeducationpage),
    path('editeducation/<int:user_id>', views.editeducation),
    path('editadditionalpage/<int:user_id>', views.editadditionalpage),
    path('editadditional/<int:user_id>', views.editadditional),
    path('editpicture/<int:user_id>', views.editpicture),
    path('logout', views.logout),
]