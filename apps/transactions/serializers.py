from rest_framework import serializers
from .models import (
    TransactionCart, TransactionCartItem, 
    TransactionPayment, TransactionReceipt, TransactionItem
)
from apps.catalogues.serializers import RobloxProductSerializer

class TransactionCartItemSerializer(serializers.ModelSerializer):
    product_details = RobloxProductSerializer(source='product', read_only=True)

    class Meta:
        model = TransactionCartItem
        fields = ['id', 'product', 'product_details', 'quantity', 'price', 'created_at']

class TransactionCartSerializer(serializers.ModelSerializer):
    items = TransactionCartItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = TransactionCart
        fields = ['id', 'user_id', 'sub_total', 'status', 'status_display', 'items', 'created_at']
        read_only_fields = ['id', 'created_at']


class TransactionPaymentSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    class Meta:
        model = TransactionPayment
        fields = ['id', 'category', 'category_display', 'name', 'created_at', 'updated_at']


class TransactionItemSerializer(serializers.ModelSerializer):
    product_details = RobloxProductSerializer(source='product', read_only=True)
    class Meta:
        model = TransactionItem
        fields = ['id', 'product', 'product_details', 'quantity', 'product_name_snapshot', 'price_snapshot', 'created_at']


class TransactionReceiptSerializer(serializers.ModelSerializer):
    receipt_items = TransactionItemSerializer(many=True, read_only=True)
    payment_details = TransactionPaymentSerializer(source='payment', read_only=True)
    class Meta:
        model = TransactionReceipt
        fields = [
            'id', 'user_id', 'roblox_account_id', 'payment', 'payment_details',
            'order_id', 'status', 'sub_total', 'total', 'receipt_items', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_id', 'created_at', 'updated_at']