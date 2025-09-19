from .models import CustomUser, Profile, Follow
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser) 
def create_profile(sender, instance, created, **kwargs): 
    """Create a profile when a new user is created.""" 
    if created: 
        Profile.objects.create(user=instance)
        


@receiver(post_save, sender=CustomUser) 
def save_profile(sender, instance, **kwargs): 
    """Save the profile whenever the user is saved.""" 
    if hasattr(instance, "profile"): 
        instance.profile.save()


