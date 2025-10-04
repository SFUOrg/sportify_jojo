# models.py (продолжение)
from django.db import models
from .profile import Profile

class ProfilePhoto(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='profile_photos/gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_main = models.BooleanField(default=False, help_text="Главное фото?")

    def __str__(self):
        return f"Photo for {self.profile.user.username} - {self.uploaded_at}"

    class Meta:
        ordering = ['-uploaded_at']