from django.shortcuts import get_object_or_404
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

class RobloxCategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = RobuxCategory.objects.all()
        serializer = RobuxCategorySerializer(categories, many=True)
        return Response({
            "message": "Daftar kategori robux",
            "data": serializer.data
        })
        
    def post(self, request):
        serializer = RobuxCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RobloxCategoryDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get_object(self, pk):
        return get_object_or_404(RobuxCategory, pk=pk)

    def get(self, request, pk):
        categories = self.get_object(pk)
        serializer = RobuxCategorySerializer(categories)
        return Response({
            "message": "Detail kategori ditemukan",
            "data": serializer.data
        })

    def put(self, request, pk):
        categories = self.get_object(pk)
        serializer = RobuxCategorySerializer(categories, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        categories = self.get_object(pk)
        categories.delete()
        return Response({
            "message": "Kategori berhasil dihapus"
        },status=status.HTTP_204_NO_CONTENT)

class RobloxRobuxListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        robux = RobloxRobux.objects.all()
        serializer = RobloxRobuxSerializer(robux, many=True)
        return Response({
            "message": "Daftar robux Roblox",
            "data": serializer.data
        })
        
    def post(self, request):
        serializer = RobloxRobuxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RobloxRobuxDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get_object(self, pk):
        return get_object_or_404(RobloxRobux, pk=pk)

    def get(self, request, pk):
        robux = self.get_object(pk)
        serializer = RobloxRobuxSerializer(robux)
        return Response({
            "message": "Detail robux ditemukan",
            "data": serializer.data
        })

    def put(self, request, pk):
        robux = self.get_object(pk)
        serializer = RobloxRobuxSerializer(robux, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        robux = self.get_object(pk)
        robux.delete()
        return Response({
            "message": "Robux berhasil dihapus"
        },status=status.HTTP_204_NO_CONTENT)

class RobloxItemListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        items = RobloxItem.objects.all()
        serializer = RobloxItemSerializer(items, many=True)
        return Response({
            "message": "Daftar item Roblox",
            "data": serializer.data
        })
        
    def post(self, request):
        serializer = RobloxItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RobloxItemDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get_object(self, pk):
        return get_object_or_404(RobloxItem, pk=pk)

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = RobloxItemSerializer(item)
        return Response({
            "message": "Detail item ditemukan",
            "data": serializer.data
        })

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = RobloxItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response({
            "message": "Item berhasil dihapus"
        },status=status.HTTP_204_NO_CONTENT)
        
class RobloxProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = RobloxProduct.objects.all()
        serializer = RobloxProductSerializer(products, many=True)
        return Response({
            "message": "Daftar produk Roblox",
            "data": serializer.data
        })
    
class RobloxProductDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get_object(self, pk):
        return get_object_or_404(RobloxProduct, pk=pk)

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = RobloxProductSerializer(product)
        return Response({
            "message": "Detail produk ditemukan",
            "data": serializer.data
        })