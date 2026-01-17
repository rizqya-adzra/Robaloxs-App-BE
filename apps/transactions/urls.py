from django.urls import path
from apps.transactions.views import CartView, CartItemView, CheckoutView, PaymentConfirmationView, PaymentMethodView, TransactionHistoryView

urlpatterns = [
    path('transaction/cart/', CartView.as_view(), name='cart-detail'),
    path('transaction/cart-item/', CartItemView.as_view(), name='cart-item-add'),
    path('transaction/cart-item/<int:pk>/', CartItemView.as_view(), name='cart-item-delete'),
    path('transaction/payments/', PaymentMethodView.as_view(), name='payment-list'),
    path('transaction/checkout/', CheckoutView.as_view(), name='checkout-process'),
    path('transaction/history/', TransactionHistoryView.as_view(), name='transaction-history'),
    path('transaction/payment/confirm/<int:order_id>/', PaymentConfirmationView.as_view(), name='payment-confirmation'),
]