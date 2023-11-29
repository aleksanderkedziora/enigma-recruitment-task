"""
Views for the user API.
"""

from rest_framework import generics

from apps.accounts.serializers import (
    UserSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Creates a new user in the system."""
    serializer_class = UserSerializer
