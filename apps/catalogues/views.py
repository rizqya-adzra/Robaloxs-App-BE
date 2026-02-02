from rest_framework import generics, permissions, status
from apps.catalogues.models import RobuxCategory, RobloxItem, RobloxProduct, RobloxRobux
from .serializers import (
    RobloxItemSerializer, 
    RobloxRobuxSerializer, 
    RobloxProductSerializer, 
    RobuxCategorySerializer
)
from utils.response import response_success 

class RobloxCategoryList(generics.ListCreateAPIView):
    queryset = RobuxCategory.objects.all()
    serializer_class = RobuxCategorySerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response_success("Daftar kategori robux", response.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response_success("Kategori berhasil dibuat", response.data, status.HTTP_201_CREATED)

class RobloxCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RobuxCategory.objects.all()
    serializer_class = RobuxCategorySerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response_success("Detail kategori ditemukan", response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return response_success("Kategori berhasil diupdate", response.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return response_success("Kategori berhasil dihapus", status_code=status.HTTP_204_NO_CONTENT)


class RobloxRobuxList(generics.ListCreateAPIView):
    queryset = RobloxRobux.objects.all()
    serializer_class = RobloxRobuxSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response_success("Daftar robux Roblox", response.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response_success("Paket Robux berhasil dibuat", response.data, status.HTTP_201_CREATED)

class RobloxRobuxDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RobloxRobux.objects.all()
    serializer_class = RobloxRobuxSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response_success("Detail robux ditemukan", response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return response_success("Paket Robux berhasil diupdate", response.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return response_success("Paket Robux berhasil dihapus", status_code=status.HTTP_204_NO_CONTENT)


class RobloxItemList(generics.ListCreateAPIView):
    queryset = RobloxItem.objects.all()
    serializer_class = RobloxItemSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response_success("Daftar item Roblox", response.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response_success("Item berhasil dibuat", response.data, status.HTTP_201_CREATED)


class RobloxItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RobloxItem.objects.all()
    serializer_class = RobloxItemSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response_success("Detail item ditemukan", response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return response_success("Item berhasil diupdate", response.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return response_success("Item berhasil dihapus", status_code=status.HTTP_204_NO_CONTENT)


class RobloxProductList(generics.ListAPIView):
    serializer_class = RobloxProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return RobloxProduct.objects.select_related('robloxrobux', 'robloxitem').all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response_success("Daftar semua produk (Item & Robux)", response.data)

class RobloxProductDetail(generics.RetrieveAPIView):
    serializer_class = RobloxProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return RobloxProduct.objects.select_related('robloxrobux', 'robloxitem').all()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response_success("Detail produk ditemukan", response.data)