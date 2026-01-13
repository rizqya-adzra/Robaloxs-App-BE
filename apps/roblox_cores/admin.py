from django.contrib import admin
from .models import RobloxServer, RobloxAccount

@admin.register(RobloxServer)
class RobloxServerAdmin(admin.ModelAdmin):
    list_display = ('id', 'server_id', 'name', 'created_at')
    search_fields = ('server_id', 'name')
    list_filter = ('created_at',)
    ordering = ('server_id',)
    
@admin.register(RobloxAccount)
class RobloxAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'roblox_user_id', 'username', 'display_name', 'avatar_url', 'created_at')
    search_fields = ('user_id', 'roblox_user_id')
    list_filter = ('created_at',)
    ordering = ('username',)