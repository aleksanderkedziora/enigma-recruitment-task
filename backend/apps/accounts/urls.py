from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.accounts import views

urlpatterns = [
    path('', views.CreateUserView.as_view()),
]
