import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from typing import ClassVar
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from enum import Enum


class PermissionType(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    

class Org(models.Model):
    """
    Represents an organization that can have multiple users.
    """
    
    name = models.CharField(max_length=255)
    
    created = models.DateTimeField(editable=False, auto_now_add=True)
    
    enabled = models.BooleanField(default=True)
    
    admin_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='admin_organizations')
    
    extid = models.UUIDField(
        verbose_name="ExtID",
        help_text="Automatically genered unique id for external identification",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    """ Automatically genered unique id for external identification """

    class Meta:
        indexes = [
            models.Index(fields=['extid']),
        ]
    
    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    """
    Default custom user model.
    """    

    # First and last name do not cover name patterns around the globe
    # name = models.CharField(_("Name of User"), blank=True, max_length=255)
    # first_name = None  # type: ignore[assignment]
    # last_name = None  # type: ignore[assignment]
    # email = models.EmailField(_("email address"), unique=True)
    # username = None  # type: ignore[assignment]
    created = models.DateTimeField(editable=False, auto_now_add=True)

    # EMAIL_FIELD = 'email'
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()
    
    extid = models.UUIDField(
        verbose_name="ExtID",
        help_text="Automatically genered unique id for external identification",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    """ Automatically genered unique id for external identification. """

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Membership(models.Model):
    """
    Represents a membership of a user to an organization with specific permissions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='memberships')
    permission = models.CharField(max_length=10, choices=[(tag, tag.value) for tag in PermissionType])
    created = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        unique_together = ('user', 'org')

    def __str__(self) -> str:
        return f"{self.user.name} - {self.org.name} ({self.permission})"