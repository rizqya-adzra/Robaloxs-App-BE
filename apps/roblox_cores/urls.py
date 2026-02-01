from django.urls import path
from apps.roblox_cores.views import (RobloxServerList, RobloxServerDetail, RobloxAccountList, RobloxAccountDetail)

urlpatterns = [
    path('roblox/servers/', RobloxServerList.as_view(), name='roblox-server-list'),
    path('roblox/servers/<int:pk>/', RobloxServerDetail.as_view(), name='roblox-server-detail'),
    path('roblox/accounts/', RobloxAccountList.as_view(), name='roblox-account-list'),
    path('roblox/accounts/<int:pk>/', RobloxAccountDetail.as_view(), name='roblox-account-detail'),
]