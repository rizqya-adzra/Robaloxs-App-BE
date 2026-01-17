from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.roblox_cores.models import RobloxServer

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# 1. Tabel: roblox_robux_categories
class RobuxCategory(TimeStampedModel):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'roblox_robux_categories'
        verbose_name_plural = 'Robux Categories'

    def __str__(self):
        return self.name

# 2. Tabel: roblox_products
class RobloxProduct(TimeStampedModel):
    class ProductType(models.TextChoices):
        ROBUX = 'robux', _('Robux')
        ITEM = 'item', _('Item')

    price = models.DecimalField(max_digits=12, decimal_places=2) 
    name = models.CharField(max_length=255)
    
    product_type = models.CharField(
        max_length=10,
        choices=ProductType.choices,
        db_column='type' 
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'roblox_products'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name} - {self.get_product_type_display()}"

# 3. Tabel: roblox_robuxs
class RobloxRobux(RobloxProduct):
    category = models.ForeignKey(
        RobuxCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='robux_packages',
        db_column='roblox_robux_category_id'
    )
    robux_amount = models.BigIntegerField()

    class Meta:
        db_table = 'roblox_robuxs'
        verbose_name_plural = 'Robux'

    def __str__(self):
        return f"{self.robux_amount} Robux ({self.name})"


# 4. Tabel: roblox_items
class RobloxItem(RobloxProduct):
    server = models.ForeignKey(
        RobloxServer,
        on_delete=models.CASCADE,
        db_column='roblox_server_id'
    )
    
    roblox_item_id_external = models.BigIntegerField(help_text="ID Item dari API Roblox")
    
    description = models.TextField(blank=True, null=True) 
    image_url = models.ImageField(upload_to='assets/images/roblox_items/', null=True, blank=True)

    class Meta:
        db_table = 'roblox_items'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.name