from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from apps.users.serializers import RegisterSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Registrasi berhasil",
                "data": {
                    "email": user.email,
                    "token": token.key
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data 
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login berhasil",
                "data": {
                    "email": user.email,
                    "token": token.key,
                    "is_staff": user.is_staff
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None 

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "Logout berhasil"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Gagal logout"}, status=status.HTTP_400_BAD_REQUEST)