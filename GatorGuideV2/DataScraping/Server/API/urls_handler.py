from django.urls import path
from . import views_handler

urlpatterns = [
    path('user/create', views_handler.create_user, name = "create"),
    path('user/delete', views_handler.delete_user, name = "delete"),
    path('user/update', views_handler.update_user, name = "delete")
]