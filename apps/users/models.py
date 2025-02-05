from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Added related_name to avoid conflict
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.')
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Added related_name to avoid conflict
        blank=True,
        help_text=_('Specific permissions for this user.')
    )
    bio = models.TextField(max_length=500, blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    total_files_processed = models.IntegerField(default=0)
    storage_used = models.BigIntegerField(default=0)  # in bytes
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return f"{settings.STATIC_URL}img/default-avatar.png"

    def __str__(self):
        return f"{self.user.username}'s profile"
