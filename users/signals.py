from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from .models import User, UserInfo


@receiver(post_save, sender=User)
def user_create_info(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, "info"):
            info = UserInfo()
            info.user = instance
            info.join_at = now()
            info.save()

            instance.info = info
