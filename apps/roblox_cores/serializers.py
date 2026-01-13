from rest_framework import serializers
from .models import RobloxServer, RobloxAccount

class RobloxServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobloxServer
        fields = '__all__'

class RobloxAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobloxAccount
        fields = '__all__'