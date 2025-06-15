# profile_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from ..models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        # Falls RegistrationSerializer es nicht tut
        Profile.objects.create(
            user=instance,
            type='customer',
            file=None, location='', tel='',
            description='', working_hours=''
        )