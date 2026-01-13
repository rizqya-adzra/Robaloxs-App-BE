from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser

from .models import RobuxCategory, RobloxItem, RobloxProduct, RobloxRobux, RobloxServer
from .serializers import RobloxItemSerializer, RobloxRobuxSerializer, RobloxProductSerializer, RobloxServerSerializer, RobuxCategorySerializer

class RobloxServerListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        items = RobloxServer.objects.all()
        serializer = RobloxServerSerializer(items, many=True)

        return Response({
            "message": "Daftar item Roblox",
            "data": {
                "server": serializer.name,
                "name": serializer.name,
                "description": serializer.name,
                "image_url": serializer.name,
            }
        })
        
class RobloxItemListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        items = RobloxItem.objects.all()
        serializer = RobloxItemSerializer(items, many=True)

        return Response({
            "message": "Daftar item Roblox",
            "data": {
                "server": serializer.server_id,
                "name": serializer.name,
                "description": serializer.name,
                "image_url": serializer.name,
            }
        })