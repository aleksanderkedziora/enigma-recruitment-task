"""
Serializers for the user API.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

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
        read_only_fields = ['is_staff']

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        user = self.context['request'].user

        if user.is_authenticated and user.is_staff:
            validated_data.update({'is_staff': True})

        return get_user_model().objects.create_user(**validated_data)


class OrderUserSerializer(serializers.ModelSerializer):
    """Serializer for fill user first and last name if they're blank."""

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Serializer for the user change password."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ['old_password', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
