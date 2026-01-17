from django.db import models
from apps.catalogues.models import RobloxProduct

class TransactionCart(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    user_id = models.BigIntegerField()
    sub_total = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transaction_carts'
        verbose_name = 'Transaction Cart'
        verbose_name_plural = 'Transaction Carts'
        ordering = ['-created_at']

    def __str__(self):
        return f"Cart {self.id} - User {self.user_id} ({self.status})"

class TransactionCartItem(models.Model):
    transaction_cart = models.ForeignKey(
        TransactionCart, 
        related_name='items', 
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        RobloxProduct, 
        on_delete=models.CASCADE,
        related_name='cart_items',
        db_column='roblox_product_id'
    )
    quantity = models.IntegerField()
    price = models.IntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transaction_cart_items'
        verbose_name = 'Transaction Cart Item'
        verbose_name_plural = 'Transaction Cart Items'

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) in Cart {self.transaction_cart_id}"

class TransactionPayment(models.Model):
    CATEGORY_CHOICES = [
        ('bank', 'Bank'),
        ('e_wallet', 'E-Wallet'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=255)
    image_url = models.ImageField(upload_to='assets/icons/payment_method/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transaction_payments'
        verbose_name = 'Transaction Payment'
        verbose_name_plural = 'Transaction Payments'

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class TransactionReceipt(models.Model):
    user_id = models.BigIntegerField()
    roblox_account_id = models.BigIntegerField()
    payment = models.ForeignKey(
        TransactionPayment, 
        on_delete=models.PROTECT,
        related_name='receipts'
    )
    order_id = models.BigIntegerField(unique=True)
    status = models.CharField(max_length=20)
    sub_total = models.IntegerField()
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transaction_receipts'
        verbose_name = 'Transaction Receipt'
        verbose_name_plural = 'Transaction Receipts'
        ordering = ['-created_at']

    def __str__(self):
        return f"Receipt {self.order_id} - {self.status}"

class TransactionItem(models.Model):
    transaction_receipt = models.ForeignKey(
        TransactionReceipt, 
        related_name='receipt_items', 
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        RobloxProduct, 
        on_delete=models.CASCADE,
        related_name='ordered_items',
        db_column='roblox_product_id'
    )
    product_name_snapshot = models.CharField(max_length=255) 
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transaction_items'
        verbose_name = 'Transaction Item'
        verbose_name_plural = 'Transaction Items'

    def __str__(self):
        return f"Item for Receipt {self.transaction_receipt.order_id}"