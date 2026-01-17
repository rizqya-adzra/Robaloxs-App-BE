from django.contrib import admin
from .models import (
    TransactionCart, TransactionCartItem, 
    TransactionPayment, TransactionReceipt, TransactionItem
)

# --- INLINES ---
# Membuat item bisa diedit langsung di dalam halaman induknya

class TransactionCartItemInline(admin.TabularInline):
    model = TransactionCartItem
    extra = 0  # Tidak menambah baris kosong tambahan secara otomatis
    readonly_fields = ['created_at']

class TransactionItemInline(admin.TabularInline):
    model = TransactionItem
    extra = 0
    readonly_fields = ['created_at']


# --- ADMIN MODELS ---

@admin.register(TransactionCart)
class TransactionCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'sub_total', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user_id', 'id']
    inlines = [TransactionCartItemInline]
    ordering = ['-created_at']

@admin.register(TransactionPayment)
class TransactionPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'updated_at']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(TransactionReceipt)
class TransactionReceiptAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user_id', 'payment', 'status', 'total', 'created_at']
    list_filter = ['status', 'payment', 'created_at']
    search_fields = ['order_id', 'user_id', 'roblox_account_id']
    readonly_fields = ['order_id', 'created_at', 'updated_at'] # Order ID tidak boleh diubah manual
    inlines = [TransactionItemInline]
    ordering = ['-created_at']

    # Memberi warna pada status di admin (Opsional/Advance)
    def get_status_color(self, obj):
        # Logika custom warna bisa ditambahkan di sini
        pass

@admin.register(TransactionItem)
class TransactionItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'transaction_receipt', 'quantity', 'created_at']
    list_filter = ['created_at']

@admin.register(TransactionCartItem)
class TransactionCartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'transaction_cart', 'product', 'quantity', 'price']