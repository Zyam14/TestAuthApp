from django.urls import path
from .views import login, delete_user

urlpatterns = [
    path("login/", login),
    path("delete/", delete_user),
]