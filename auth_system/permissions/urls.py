from django.urls import path
from .views import create_rule

urlpatterns = [
    path("rules/create/", create_rule),
]