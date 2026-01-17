from django.contrib import admin
from apps.catalogues.models import RobuxCategory, RobloxItem, RobloxProduct, RobloxRobux

@admin.register(RobuxCategory)
class RobuxCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(RobloxRobux)
class RobloxRobuxAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'robux_amount', 'price', 'category', 'is_active', 'updated_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('name', 'robux_amount')
    list_select_related = ('category',)
    fieldsets = (
        ('Product General', {
            'fields': ('name', 'price', 'is_active', 'product_type')
        }),
        ('Robux Details', {
            'fields': ('robux_amount', 'category')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) 
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'product_type')
    def save_model(self, request, obj, form, change):
        if not obj.product_type:
            obj.product_type = RobloxProduct.ProductType.ROBUX
        super().save_model(request, obj, form, change)

@admin.register(RobloxItem)
class RobloxItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'server', 'price', 'roblox_item_id_external', 'is_active')
    list_filter = ('is_active', 'server')
    search_fields = ('name', 'roblox_item_id_external')
    list_select_related = ('server',)
    fieldsets = (
        ('Product General', {
            'fields': ('name', 'price', 'is_active', 'product_type')
        }),
        ('Item Details', {
            'fields': ('server', 'roblox_item_id_external', 'description', 'image_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'product_type')
    def save_model(self, request, obj, form, change):
        if not obj.product_type:
            obj.product_type = RobloxProduct.ProductType.ITEM
        super().save_model(request, obj, form, change)

@admin.register(RobloxProduct)
class RobloxProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'product_type', 'is_active', 'get_detail_info')
    list_filter = ('product_type', 'is_active')
    search_fields = ('name',)
    
    def get_detail_info(self, obj):
        if obj.product_type == RobloxProduct.ProductType.ROBUX:
            try:
                return f"{obj.robloxrobux.robux_amount} Robux"
            except:
                return "-"
        elif obj.product_type == RobloxProduct.ProductType.ITEM:
            try:
                return f"Server: {obj.robloxitem.server.name}"
            except:
                return "-"
        return "-"
    get_detail_info.short_description = "Detail Info"

    def has_add_permission(self, request):
        return False