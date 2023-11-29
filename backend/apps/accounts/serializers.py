"""
Serializers for the user API.
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'is_staff']
        extra_kwargs = {
            'password':
                {'write_only': True, 'min_length': 5}
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)


class OrderUserSerializer(serializers.ModelSerializer):
    """Serializer for fill user first and last name if they're blank."""

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']

