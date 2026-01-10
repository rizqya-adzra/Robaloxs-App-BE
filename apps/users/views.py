from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser

from .models import UserProfile, UserPrivateData
from .serializers import RegisterSerializer, UserProfileSerializer, UserPrivateDataSerializer

# 1. REGISTER VIEW 
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                "message": "Registrasi berhasil",
                "data": {
                "email": user.email,
                "token": token.key
            }}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. LOGIN VIEW
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login berhasil",
                "data": {
                "email": user.email,
                "token": token.key,
                "is_staff": user.is_staff
            }})
        
        return Response({"error": "Email atau password salah"}, status=status.HTTP_400_BAD_REQUEST)

# 3. LOGOUT VIEW
class LogoutView(APIView):
    uthentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "Logout berhasil"})
        except:
            return Response({"message": "Terjadi kesalahan saat logout"}, status=status.HTTP_400_BAD_REQUEST)

# 4. PROFILE VIEW
class MyProfileView(APIView):
    uthentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        user = request.user
        
        profile = getattr(user, 'profile', None)
        private_data = getattr(user, 'private_data', None)
        current_badge = getattr(user, 'badge', None)
        badge_data = None
        if current_badge:
            badge_data = {
                "name": current_badge.name,
                "level": current_badge.level,
                "description": current_badge.description,
                "category": current_badge.category,
            }
            
        avatar_link = None
        if profile and profile.avatar_url:
            avatar_link = request.build_absolute_uri(profile.avatar_url.url)
            
        data = {
            "email": user.email,
            "is_staff": user.is_staff,
            "avatar_url": avatar_link,
            "total_spendings": profile.total_spendings if profile else 0,
            "full_name": private_data.full_name if private_data else "",
            "telephone": private_data.telephone if private_data else "",
            "badge": badge_data
        }
        return Response({
            "message": "Berhasil mengambil data profil",
            "data": data
        })

    def put(self, request):
        user = request.user
        
        private_data, _ = UserPrivateData.objects.get_or_create(user=user)
        profile, _ = UserProfile.objects.get_or_create(user=user)

        private_serializer = UserPrivateDataSerializer(private_data, data=request.data, partial=True)
        profile_serializer = UserProfileSerializer(profile, data=request.data, partial=True)

        is_private_valid = private_serializer.is_valid()
        is_profile_valid = profile_serializer.is_valid()

        if is_private_valid and is_profile_valid:
            private_serializer.save()
            profile_serializer.save()
            
        avatar_link = None
        if profile and profile.avatar_url:
            avatar_link = request.build_absolute_uri(profile.avatar_url.url)
            
            return Response({
                "message": "Profil Berhasil di update",
                "data": {
                    "username": profile.username,
                    "full_name": private_data.full_name,
                    "telephone": private_data.telephone,
                    "avatar_url": avatar_link,
                }
            })
        
        errors = {}
        if not is_private_valid:
            errors['private_errors'] = private_serializer.errors
        if not is_profile_valid:
            errors['profile_errors'] = profile_serializer.errors

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)