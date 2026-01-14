from django.urls import path
from apps.catalogues.views import RobloxCategoryListView, RobloxCategoryDetailView, RobloxItemDetailView, RobloxProductDetailView, RobloxProductListView, RobloxRobuxDetailView, RobloxRobuxListView, RobloxItemListView

urlpatterns = [
    path('roblox/categories/', RobloxCategoryListView.as_view(), name='roblox_categories'),
    path('roblox/categories/<int:pk>/', RobloxCategoryDetailView.as_view(), name='roblox_category_detail'),
    path('roblox/robux/', RobloxRobuxListView.as_view(), name='roblox_robux'),
    path('roblox/robux/<int:pk>/', RobloxRobuxDetailView.as_view(), name='roblox_robux_detail'),
    path('roblox/items/', RobloxItemListView.as_view(), name='roblox_items'),
    path('roblox/items/<int:pk>/', RobloxItemDetailView.as_view(), name='roblox_items'),
    path('roblox/products/', RobloxProductListView.as_view(), name='roblox_products'),
    path('roblox/products/<int:pk>/', RobloxProductDetailView.as_view(), name='roblox_product_detail'),
]