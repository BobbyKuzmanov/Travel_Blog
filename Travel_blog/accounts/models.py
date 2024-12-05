from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
import os

UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(UserModel, editable=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=True,)
    last_name = models.CharField(max_length=20, blank=True,)
    email = models.EmailField(blank=True,)
    about_me = models.TextField(default='', blank=True,)
    profile_image = models.ImageField(
        upload_to='profiles',
        blank=True,
    )

    def save(self, *args, **kwargs):
        # If this is an update and there's a new image
        if self.pk:
            try:
                old_profile = Profile.objects.get(pk=self.pk)
                if old_profile.profile_image and self.profile_image != old_profile.profile_image:
                    # Delete the old image file
                    if os.path.isfile(old_profile.profile_image.path):
                        os.remove(old_profile.profile_image.path)
            except Profile.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the profile image file when the profile is deleted
        if self.profile_image:
            if os.path.isfile(self.profile_image.path):
                os.remove(self.profile_image.path)
        super().delete(*args, **kwargs)
