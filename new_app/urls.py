# from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('user_page', views.user_page),
    path('add_thought', views.add_thought),
    path('details/<int:thought_id>', views.details),
    path('like/<int:thought_id>', views.like),
    path('unlike/<int:thought_id>', views.unlike),
    path('logout', views.logout),
    path('delete/<int:thought_id>', views.delete)
    
]