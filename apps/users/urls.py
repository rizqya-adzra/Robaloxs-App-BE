from django.urls import path
from apps.users.views.authentications import RegisterView, LoginView, LogoutView
from apps.users.views.profiles import MyProfileView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('profile/', MyProfileView.as_view(), name='my-profile'),
]