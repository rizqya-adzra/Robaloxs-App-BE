from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.transactions.models import TransactionCart, TransactionCartItem
from apps.transactions.serializers import (
    TransactionCartSerializer, 
    TransactionCartItemSerializer, 
    AddToCartSerializer,
)
from utils.response import response_success, response_error

class CartView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionCartSerializer

    def get_object(self):
        cart, _ = TransactionCart.objects.get_or_create(
            user_id=self.request.user.id,
            status='pending',
            defaults={'sub_total': 0}
        )
        return cart

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response_success(message="Data keranjang berhasil diambil", data=serializer.data)


class CartItemView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddToCartSerializer
        return TransactionCartItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            cart_item = serializer.save()
            
            result_serializer = TransactionCartItemSerializer(cart_item)
            return response_success(
                message="Item berhasil ditambahkan ke keranjang",
                data=result_serializer.data,
                status_code=201
            )
        return response_error(
            message="Gagal menambahkan item",
            errors=serializer.errors
        )

    def delete(self, request, pk, *args, **kwargs):
        try:
            cart_item = TransactionCartItem.objects.get(id=pk, transaction_cart__user_id=request.user.id)
            cart = cart_item.transaction_cart
            cart_item.delete()
            
            total = sum(item.quantity * item.price for item in cart.items.all())
            cart.sub_total = total
            cart.save()

            return response_success(message="Item berhasil dihapus dari keranjang")
        except TransactionCartItem.DoesNotExist:
            return response_error(message="Item tidak ditemukan", status_code=404)