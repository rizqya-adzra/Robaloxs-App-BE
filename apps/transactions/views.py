from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from django.shortcuts import get_object_or_404
import uuid

from .models import TransactionCart, TransactionCartItem, RobloxProduct, TransactionPayment, TransactionItem, TransactionReceipt
from .serializers import TransactionCartSerializer, TransactionCartItemSerializer, TransactionPaymentSerializer, TransactionReceiptSerializer, TransactionReceiptSerializer

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart, created = TransactionCart.objects.get_or_create(
            user_id=user.id, 
            status='pending',
            defaults={'sub_total': 0}
        )
        serializer = TransactionCartSerializer(cart)
        return Response(serializer.data)

class CartItemView(APIView):    
    @transaction.atomic
    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        if not all([user.id, product_id]):
            return Response({"error": "user_id and product_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(RobloxProduct, id=product_id, is_active=True)
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
        return Response({
            "message": "Item added to cart",
            "cart_item": TransactionCartItemSerializer(cart_item).data
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        cart_item = get_object_or_404(TransactionCartItem, id=pk)
        cart = cart_item.transaction_cart
        cart_item.delete()
        
        self._update_cart_total(cart)
        return Response({"message": "Item removed"}, status=status.HTTP_204_NO_CONTENT)

    def _update_cart_total(self, cart):
        total = sum(item.quantity * item.price for item in cart.items.all())
        cart.sub_total = total
        cart.save()
        
class PaymentMethodView(APIView):
    def get(self, request):
        payments = TransactionPayment.objects.all()
        serializer = TransactionPaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TransactionPaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Metode pembayaran berhasil ditambahkan!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CheckoutView(APIView):
    @transaction.atomic
    def post(self, request):
        user_id = request.user.id
        payment_id = request.data.get('payment_id')
        roblox_account_id = request.data.get('roblox_account_id')

        cart = get_object_or_404(TransactionCart, user_id=user_id, status='pending')

        item_ids = request.data.get('item_ids', [])
        
        selected_items = TransactionCartItem.objects.filter(
            id__in=item_ids,
            transaction_cart__user_id=user_id,
            transaction_cart__status='pending'
        )

        if not selected_items.exists():
            return Response({"error": "Items tidak ditemukan"}, status=404)

        sub_total_selected = sum(item.quantity * item.price for item in selected_items)

        payment = get_object_or_404(TransactionPayment, id=payment_id)
        receipt = TransactionReceipt.objects.create(
            user_id=user_id,
            roblox_account_id=roblox_account_id,
            payment=payment,
            order_id=int(uuid.uuid4().int >> 96),
            status='unpaid',
            sub_total=sub_total_selected,
            total=sub_total_selected
        )

        transaction_items_to_create = []
        for item in selected_items:
            transaction_items_to_create.append(
                TransactionItem(
                    transaction_receipt=receipt,
                    product=item.product,         
                    quantity=item.quantity,
                    price_snapshot=item.price,      
                    product_name_snapshot=item.product.name
                )
            )
        TransactionItem.objects.bulk_create(transaction_items_to_create)

        selected_items.delete()

        self._update_cart_total(cart)

        serializer = TransactionReceiptSerializer(receipt)
        return Response({"message": "Checkout berhasil", "receipt": serializer.data})

    def _update_cart_total(self, cart):
        total = sum(item.quantity * item.price for item in cart.items.all())
        cart.sub_total = total
        cart.save()
        
class PaymentConfirmationView(APIView):
    def post(self, request, order_id):
        receipt = get_object_or_404(TransactionReceipt, order_id=order_id)
        
        receipt.status = 'paid'
        receipt.save()
        
        return Response({
            "message": f"Order {order_id} sudah berhasil terbayar!",
            "status": receipt.status
        })

class TransactionHistoryView(APIView):
    def get(self, request):
        user_id = request.user.id
        receipts = TransactionReceipt.objects.filter(user_id=user_id).order_by('-created_at')
        serializer = TransactionReceiptSerializer(receipts, many=True)
        return Response({"message": "Riwayat Transaksi", "data": serializer.data})