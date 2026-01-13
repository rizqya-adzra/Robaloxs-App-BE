from django.urls import path
from apps.roblox_cores.views import (RobloxServerListView, RobloxServerDetailView, RobloxAccountListView, RobloxAccountDetailView)

urlpatterns = [
    path('roblox/servers/', RobloxServerListView.as_view(), name='roblox-server-list'),
    path('roblox/servers/<int:pk>/', RobloxServerDetailView.as_view(), name='roblox-server-detail'),
    path('roblox/accounts/', RobloxAccountListView.as_view(), name='roblox-account-list'),
    path('roblox/accounts/<int:pk>/', RobloxAccountDetailView.as_view(), name='roblox-account-detail'),
]