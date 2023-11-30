"""
Views for the user API.
"""
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.permission import IsStaffOrNotAuthenticated
from apps.accounts.serializers import (
    UserSerializer, ChangePasswordSerializer,
)


class RegisterView(generics.CreateAPIView):
    """Creates a new user in the system."""
    serializer_class = UserSerializer
    permission_classes = [IsStaffOrNotAuthenticated]


class ChangePasswordView(generics.UpdateAPIView):
    """Changes request user password."""
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
