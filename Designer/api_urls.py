from django.urls import path
from . import views

urlpatterns = [
    path('get-styles/', views.get_styles_api),
    path('add-style/', views.add_style_api),
    path('regenerate-code/', views.regenerate_code_api),
    path('delete-style/', views.delete_style_api),

    path('get-hover-styles/', views.get_hover_styles_api),
    path('get-active-styles/', views.get_active_styles_api),
]