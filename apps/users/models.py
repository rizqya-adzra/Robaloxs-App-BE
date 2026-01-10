from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

# 1. Custom Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email harus diisi'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser harus memiliki is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser harus memiliki is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

# 2. Tabel: users_auth 
class User(AbstractUser):
    username = None 
    email = models.EmailField(_('email address'), unique=True)
    date_joined = None
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []      

    objects = CustomUserManager()

    class Meta:
        db_table = 'users_auth'  
        verbose_name = _('User Auth')

    def __str__(self):
        return self.email

# 3. Tabel: users_badges
class Badge(models.Model):
    class Category(models.TextChoices):
        AVATAR = 'avatar', 'Avatar'
        ACHIEVEMENT = 'achievement', 'Achievement'

    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    icon = models.ImageField(upload_to='assets/images/badges_icons/', null=True, blank=True)  
    description = models.TextField(null=True, blank=True)
    category = models.CharField(
        max_length=50, 
        choices=Category.choices, 
        default=Category.ACHIEVEMENT
    )

    class Meta:
        db_table = 'users_badges'

    def __str__(self):
        return f"{self.name} (Lv. {self.level})"

# 4. Tabel: users_profile
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        db_column='user_id'
    )
    badge = models.ForeignKey(
        Badge, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='used_by_profiles',
        db_column='badge_id'
    )
    username = models.CharField(max_length=255, null=True, blank=True)
    avatar_url = models.ImageField(upload_to='assets/images/users_avatar/', null=True, blank=True)  
    total_spendings = models.IntegerField(default=0)
    weekly_spendings = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_profile'

    def __str__(self):
        return f"Profile of {self.user.email}"

# 5. Tabel: users_private_data
class UserPrivateData(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='private_data',
        db_column='user_id'
    )
    full_name = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_private_data'
        verbose_name = "User Private Data"
        verbose_name_plural = "User Private Data"

    def __str__(self):
        return f"Private data of {self.user.email}"