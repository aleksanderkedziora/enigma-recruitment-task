from django.urls import path

from apps.accounts import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('change_password/', views.ChangePasswordView.as_view(), name='auth_change_password'),
]
