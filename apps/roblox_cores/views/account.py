from rest_framework import generics, permissions, status
from apps.roblox_cores.models import RobloxAccount
from apps.roblox_cores.serializers import RobloxAccountSerializer
from utils.response import response_success


class RobloxAccountList(generics.ListCreateAPIView):
    serializer_class = RobloxAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RobloxAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response_success("Daftar akun Roblox", response.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response_success("Akun berhasil ditambahkan", response.data, status.HTTP_201_CREATED)


class RobloxAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RobloxAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RobloxAccount.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response_success("Detail akun ditemukan", response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return response_success("Akun berhasil diupdate", response.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return response_success("Akun berhasil dihapus", status_code=status.HTTP_200_OK)