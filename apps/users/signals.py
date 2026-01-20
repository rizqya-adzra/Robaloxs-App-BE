from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import User, UserProfile, UserPrivateData

@receiver(post_save, sender=User)
def create_user_related_tables(sender, instance, created, **kwargs):
    if created:
        generated_username = instance.email.split('@')[0]
        UserProfile.objects.create(user=instance, username=generated_username)
        UserPrivateData.objects.create(user=instance)