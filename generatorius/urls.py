from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate_text/', views.generate_text, name='generate_text'),
    path('choose_text/', views.choose_text, name='choose_text'),
    path('edit_text/', views.edit_text, name='edit_text'),
    path('generate_audio/', views.generate_audio, name='generate_audio'),
    path('generate_image/', views.generate_image, name='generate_image'),
    path('choose_image/', views.choose_image, name='choose_image'),
    path('result/', views.result, name='result'),
]