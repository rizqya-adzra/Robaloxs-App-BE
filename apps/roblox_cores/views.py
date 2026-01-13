from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from .models import RobloxServer, RobloxAccount
from .serializers import RobloxServerSerializer, RobloxAccountSerializer

class RobloxServerListView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        servers = RobloxServer.objects.all()
        serializer = RobloxServerSerializer(servers, many=True)
        return Response({
            "message": "Daftar server Roblox",
            "data": serializer.data
        })

    def post(self, request):
        serializer = RobloxServerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({
                "message": "Server berhasil dibuat",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RobloxServerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(RobloxServer, pk=pk)

    def get(self, request, pk):
        server = self.get_object(pk)
        serializer = RobloxServerSerializer(server)
        return Response({
            "message": "Detail server ditemukan",
            "data": serializer.data
        })

    def put(self, request, pk):
        server = self.get_object(pk)
        serializer = RobloxServerSerializer(server, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Server berhasil diupdate",
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        server = self.get_object(pk)
        server.delete()
        return Response({
            "message": "Server berhasil dihapus"
        }, status=status.HTTP_204_NO_CONTENT)

class RobloxAccountListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        accounts = RobloxAccount.objects.filter(user=request.user)
        serializer = RobloxAccountSerializer(accounts, many=True)
        return Response({
            "message": "Daftar akun Roblox",
            "data": serializer.data
        })

    def post(self, request):
        serializer = RobloxAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RobloxAccountDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        obj = get_object_or_404(RobloxAccount, pk=pk)
        
        if obj.user != user:
            raise PermissionDenied("Kamu bukan pemilik akun ini!")
            
        return obj

    def get(self, request, pk):
        account = self.get_object(pk, request.user)
        serializer = RobloxAccountSerializer(account)
        return Response({
            "message": "Detail akun ditemukan",
            "data": serializer.data
        })

    def put(self, request, pk):
        account = self.get_object(pk, request.user) 
        serializer = RobloxAccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Akun berhasil diupdate",
                "data": serializer.data
            })
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        account = self.get_object(pk, request.user)
        account.delete()
        return Response({
            "message": "Akun berhasil dihapus"
        },status=status.HTTP_204_NO_CONTENT)