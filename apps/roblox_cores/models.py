from django.db import models
from django.conf import settings 

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# 1. Tabel: roblox_servers
class RobloxServer(TimeStampedModel):
    server_id = models.BigIntegerField(unique=True, help_text="ID Server/Game dari Roblox")
    name = models.CharField(max_length=255)
    image_url = models.ImageField(upload_to='assets/images/roblox_server/', null=True, blank=True) 

    class Meta:
        db_table = 'roblox_servers'
        verbose_name = 'Roblox Server'
        verbose_name_plural = 'Roblox Servers'

    def __str__(self):
        return f"{self.name} ({self.server_id})"

# 2. Tabel: roblox_accounts
class RobloxAccount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='roblox_accounts',
        db_column='user_id'
    )

    roblox_user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roblox_accounts'
        verbose_name = 'Roblox Account'
        verbose_name_plural = 'Roblox Accounts'
        
        indexes = [
            models.Index(fields=['roblox_user_id']),
            models.Index(fields=['username']),
        ]

    def __str__(self):
        return f"{self.username} (Linked to {self.user.email})"
    
    @property
    def website_profile(self):
        return self.user.profile