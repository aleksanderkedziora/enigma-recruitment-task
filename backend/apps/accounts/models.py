from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)

    first_name = models.CharField(_("first name"), max_length=150, null=True)
    last_name = models.CharField(_("last name"), max_length=150, null=True)

    is_staff = models.BooleanField(_("staff"), default=False,)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'auth_user'

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def delete(self, *args, hard_delete=False, **kwargs):
        if not hard_delete:
            raise Exception(f'Deleting User object is forbidden! Deactivate user {self.full_name} instead.')
        super().delete(*args, **kwargs)
