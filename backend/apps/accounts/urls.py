from django.urls import path

from apps.accounts import views

urlpatterns = [
    path('', views.CreateUserView.as_view()),
]
