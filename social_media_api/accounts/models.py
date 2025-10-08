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

    # following 
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
        help_text='Users that this user follows'
    )

    def follow(self, user):
        """Follow another user"""
        if user == self:
            return
        self.following.add(user)

    def unfollow(self, user):
        """Unfollow another user"""
        if user == self:
            return
        self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(pk=user.pk).exists()

    def _str_(self):
        return self.username

    # profile_picture
    profile_picture = models.ImageField(
        upload_to=profile_image_upload_to,
        blank=True,
        null=True
    )
    