from .models import CustomUser, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile when a new user is created.""" 
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """Save the profile whenever the user is saved.""" 
    instance.profile.save() # Ensure profile is saved whenever user is saved




