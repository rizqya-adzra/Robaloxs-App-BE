from rest_framework import serializers
from django.db import transaction
import uuid

from apps.transactions.models import (
    TransactionCart, TransactionCartItem, 
    TransactionPayment, TransactionReceipt, TransactionItem,
    RobloxProduct
)

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, default=1)
    def validate_product_id(self, value):
        if not RobloxProduct.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Produk tidak ditemukan atau tidak aktif.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        product_id = validated_data['product_id']
        quantity = validated_data['quantity']
        product = RobloxProduct.objects.get(id=product_id)
        cart, _ = TransactionCart.objects.get_or_create(
            user_id=user.id,
            status='pending',
            defaults={'sub_total': 0}
        )
        cart_item, created = TransactionCartItem.objects.get_or_create(
            transaction_cart=cart,
            product=product,
            defaults={'price': product.price, 'quantity': 0}
        )
        cart_item.quantity += quantity
        cart_item.price = product.price 
        cart_item.save()
        self._update_cart_total(cart)
        return cart_item

    def _update_cart_total(self, cart):
        total = sum(item.quantity * item.price for item in cart.items.all())
        cart.sub_total = total
        cart.save()


class CheckoutSerializer(serializers.Serializer):
    payment_id = serializers.PrimaryKeyRelatedField(
        queryset=TransactionPayment.objects.all(),
        error_messages={'does_not_exist': 'Metode pembayaran tidak valid.'}
    )
    roblox_account_id = serializers.CharField(
        min_length=3,
        error_messages={'required': 'Roblox Account ID wajib diisi.'}
    )
    item_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        error_messages={'empty': 'Pilih setidaknya satu item untuk checkout.'}
    )

    def validate(self, attrs):
        user = self.context['request'].user
        item_ids = attrs['item_ids']
        selected_items = TransactionCartItem.objects.filter(
            id__in=item_ids,
            transaction_cart__user_id=user.id,
            transaction_cart__status='pending'
        )
        if len(selected_items) != len(item_ids):
            raise serializers.ValidationError({"item_ids": "Beberapa item tidak valid atau tidak ditemukan di keranjang."})
        attrs['selected_items'] = selected_items
        attrs['cart'] = selected_items.first().transaction_cart
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        selected_items = validated_data['selected_items']
        cart = validated_data['cart']
        sub_total = sum(item.quantity * item.price for item in selected_items)
        receipt = TransactionReceipt.objects.create(
            user_id=user.id,
            roblox_account_id=validated_data['roblox_account_id'],
            payment=validated_data['payment_id'],
            order_id=int(uuid.uuid4().int >> 96), 
            status='unpaid',
            sub_total=sub_total,
            total=sub_total
        )
        transaction_items = [
            TransactionItem(
                transaction_receipt=receipt,
                product=item.product,
                quantity=item.quantity,
                price_snapshot=item.price,
                product_name_snapshot=item.product.name
            ) for item in selected_items
        ]
        TransactionItem.objects.bulk_create(transaction_items)
        selected_items.delete()
        new_cart_total = sum(item.quantity * item.price for item in cart.items.all())
        cart.sub_total = new_cart_total
        cart.save()
        return receipt