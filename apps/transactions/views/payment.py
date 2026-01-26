from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.transactions.models import TransactionReceipt, TransactionPayment
from apps.transactions.serializers import (
    TransactionPaymentSerializer, 
    CheckoutSerializer,
    TransactionReceiptSerializer
)
from utils.response import response_success, response_error

class PaymentMethodView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated] 
    queryset = TransactionPayment.objects.all()
    serializer_class = TransactionPaymentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response_success(message="List metode pembayaran", data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_success(
                message="Metode pembayaran berhasil ditambahkan", 
                data=serializer.data,
                status_code=201
            )
        return response_error(message="Gagal menambah metode pembayaran", errors=serializer.errors)


class CheckoutView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CheckoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            receipt = serializer.save() 
            receipt_serializer = TransactionReceiptSerializer(receipt)
            return response_success(
                message="Checkout berhasil", 
                data=receipt_serializer.data,
                status_code=201
            )
        return response_error(message="Checkout gagal", errors=serializer.errors)


class PaymentConfirmationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TransactionReceipt.objects.all()
    lookup_field = 'order_id'
    
    def post(self, request, order_id):
        receipt = get_object_or_404(TransactionReceipt, order_id=order_id)
        if receipt.status == 'paid':
             return response_error(message="Pesanan ini sudah dibayar sebelumnya.")
        receipt.status = 'paid'
        receipt.save()
        return response_success(
            message=f"Order {order_id} berhasil dibayar!",
            data={"status": receipt.status, "order_id": receipt.order_id}
        )


class TransactionHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionReceiptSerializer

    def get_queryset(self):
        return TransactionReceipt.objects.filter(user_id=self.request.user.id).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response_success(message="Riwayat Transaksi", data=serializer.data)