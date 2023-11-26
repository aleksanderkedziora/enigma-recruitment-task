"""
Views for the user API.
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from apps.accounts.serializers import (
    UserSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Creates a new user in the system."""
    serializer_class = UserSerializer
