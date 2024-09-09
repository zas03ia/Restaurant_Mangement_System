from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from accountio.choices import OrganizationUserRoleChoices
from .managers import UserManager

from accountio.models import Location, Organization
from shared.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="resident",
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """
        Returns the first_name plus the last_name.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()


class OrganizationUser(BaseModel):

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="organization_users"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=OrganizationUserRoleChoices.choices)

    def __str__(self):
        return f"{self.user.username} - {self.role} at {self.organization.name}"
