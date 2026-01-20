from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import User, UserProfile, UserPrivateData, Badge

# 1. Konfigurasi Inline untuk Profile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'

# 2. Konfigurasi Inline untuk Private Data
class UserPrivateDataInline(admin.StackedInline):
    model = UserPrivateData
    can_delete = False
    verbose_name_plural = 'User Private Data'
    fk_name = 'user'
    list_display = 'username'

# 3. Custom User Admin
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('get_username', 'email', 'is_staff', 'is_superuser', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'profile__username')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'created_at')}),
    )
    
    readonly_fields = ('created_at', 'last_login')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'is_staff', 'is_active')}
        ),
    )

    inlines = [UserProfileInline, UserPrivateDataInline]
    
    def get_username(self, obj):
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.username
        return "-"

# 4. Register Model Badge (Terpisah)
@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

# 5. Register User dengan konfigurasi CustomUserAdmin tadi
admin.site.register(User, CustomUserAdmin)