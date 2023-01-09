import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for Hawkshaw.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # UUID Primary Key Field
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    bio = models.TextField(blank=True)
    company = models.CharField(_("Company I Work For"), blank=True, max_length=255)
    location = models.CharField(_("Location"), blank=True, max_length=255)
    show_primary_email = models.BooleanField(default=False)
    website = models.URLField(blank=True)
    avatar = models.ImageField(blank=True, upload_to='avatar_images')
    cover_img = models.ImageField(blank=True, upload_to='cover_images')

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
