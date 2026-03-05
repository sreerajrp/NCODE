from django.urls import path
from Designer import views
from .views import get_styles_api ,add_style_api, regenerate_code_api, delete_style_api
urlpatterns = [
    path('filemanager/', views.filemanager, name = "filemanager"),
    path('createdesign/', views.createdesign, name = "createdesign"),
    path('', views.redirect_to_authorization),
    path('authorization/', views.authorization, name="authorization"),
    path('signup/',views.signup, name = "signup"),
    path('loggingin/',views.loggingin, name = "loggingin"),
    path('profilepage/',views.profilepage, name = "profilepage"),
    path('settingspage/',views.settingspage, name = "settingspage"),
    path('saveproject/',views.saveproject, name = "saveproject"),
    path('loggingout/',views.loggingout, name = "loggingout"),
    path('divdetails/',views.divdetails, name = "divdetails"),
    path('saveandexit/',views.saveandexit, name = "saveandexit"),
    path('projects/',views.projects, name = "projects"),
    path('imagedetails/',views.imagedetails, name = "imagedetails"),
    path('textdetails/',views.textdetails, name = "textdetails"),
    path('inputdetails/',views.inputdetails, name = "inputdetails"),
    path('generatecode/',views.generatecode, name = "generatecode"),
    path('deleteproject/<str:projectname>/', views.deleteproject, name='deleteproject'),
    path('deleteaccount/', views.deleteaccount, name='deleteaccount'),
    path('openproject/<str:projectname>/', views.openproject, name = "openproject"),
    path('codepage/', views.codepage, name='codepage'),

]