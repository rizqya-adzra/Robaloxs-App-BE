from django.urls import path
from apps.catalogues.views import RobloxCategoryList, RobloxCategoryDetail, RobloxItemList, RobloxItemDetail, RobloxProductList, RobloxProductDetail, RobloxRobuxList, RobloxRobuxDetail

urlpatterns = [
    path('roblox/categories/', RobloxCategoryList.as_view(), name='roblox_categories'),
    path('roblox/categories/<int:pk>/', RobloxCategoryDetail.as_view(), name='roblox_category_detail'),
    path('roblox/robux/', RobloxRobuxList.as_view(), name='roblox_robux'),
    path('roblox/robux/<int:pk>/', RobloxRobuxDetail.as_view(), name='roblox_robux_detail'),
    path('roblox/items/', RobloxItemList.as_view(), name='roblox_items'),
    path('roblox/items/<int:pk>/', RobloxItemDetail.as_view(), name='roblox_items'),
    path('roblox/products/', RobloxProductList.as_view(), name='roblox_products'),
    path('roblox/products/<int:pk>/', RobloxProductDetail.as_view(), name='roblox_product_detail'),
]