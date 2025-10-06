from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

def profile_image_upload_to(instance, filename):
    return f'profile_pictures/user_{instance.id}/{filename}'

class CustomUser(AbstractUser):
    """
    Extends Django's AbstractUser with extra fields:
    - bio: optional short biography
    - profile_picture: optional image
    - followers: ManyToMany to self (asymmetric)
    """
    # bio
    bio = models.TextField(blank=True, null=True)

    # profile_picture
    profile_picture = models.ImageField(
        upload_to=profile_image_upload_to,
        blank=True,
        null=True
    )
    # followers: users that follow this user
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    def _str_(self):
        return self.username