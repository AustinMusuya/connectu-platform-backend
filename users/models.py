from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with email instead of username."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    # profile_pic = models.ImageField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    email = models.EmailField(unique=True)  # Ensure email is unique

    # Optional username field
    username = models.CharField(max_length=50, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Set email as the primary identifier
    REQUIRED_FIELDS = []  # No other required fields apart from email

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)            
    profile_pic = models.URLField(max_length=500, blank=True, null=True) 

    def __str__(self):
        return f"{self.user.email}'s profile"
    
    # Get followers of a user
    def get_followers(self):
        return CustomUser.objects.filter(following__followed=self.user)
    
    # Get users that this user is following
    def get_following(self):
        return CustomUser.objects.filter(followers__follower=self.user)
    
    # Follow another user
    def follow(self, user_to_follow):
        if self.user != user_to_follow:
            Follow.objects.get_or_create(follower=self.user, followed=user_to_follow)
    # Unfollow another user
    def unfollow(self, user_to_unfollow):
        Follow.objects.filter(follower=self.user, followed=user_to_unfollow).delete()

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.email} follows {self.followed.email}"
    
