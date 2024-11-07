from django.db import models
from django.contrib.auth.models import AbstractUser
from typing import ClassVar
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


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

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})