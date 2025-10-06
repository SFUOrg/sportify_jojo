# sf_auth/signals.py
import os
from django.db.models.signals import post_save, post_delete
#from social_django.signals import auth_already_associated

from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, ProfilePhoto


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Создаёт Profile при создании нового User.
    """
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_delete, sender=ProfilePhoto)
def delete_profile_photo_file(sender, instance, **kwargs):
    """
    Удаляет файл изображения с диска при удалении ProfilePhoto.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(post_delete, sender=Profile)
def delete_profile_main_photo_file(sender, instance, **kwargs):
    """
    Удаляет основное фото профиля (profile_photo) при удалении Profile.
    """
    if instance.profile_photo:
        if os.path.isfile(instance.profile_photo.path):
            os.remove(instance.profile_photo.path)

# @receiver(auth_already_associated)
# def handle_auth_already_associated(sender, request, backend, *args, **kwargs):
#     # Показываем сообщение пользователю
#     messages.error(request, "Этот аккаунт Telegram уже связан с другим пользователем.")
#     # Перенаправляем на страницу входа или профиля
#     return redirect('login')