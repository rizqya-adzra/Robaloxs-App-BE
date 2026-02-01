from rest_framework import generics, permissions, status
from apps.roblox_cores.models import RobloxServer
from apps.roblox_cores.serializers import RobloxServerSerializer
from utils.response import response_success


class RobloxServerList(generics.ListCreateAPIView):
    queryset = RobloxServer.objects.all()
    serializer_class = RobloxServerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response_success("Daftar server Roblox", response.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response_success("Server berhasil dibuat", response.data, status.HTTP_201_CREATED)


class RobloxServerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RobloxServer.objects.all()
    serializer_class = RobloxServerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response_success("Detail server ditemukan", response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return response_success("Server berhasil diupdate", response.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return response_success("Server berhasil dihapus", status_code=status.HTTP_200_OK)