from django.urls import path
from . import views

urlpatterns = [
    path('user/get/', views.get_users, name='get_users'),
    path('user/create/', views.create_user, name='create_user'),
]