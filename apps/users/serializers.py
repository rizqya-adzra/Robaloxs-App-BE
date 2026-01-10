from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserProfile, UserPrivateData, Badge

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'avatar_url']
        read_only_fields = ['total_spendings', 'weekly_spendings']

class UserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        read_only_fields = ['name', 'level', 'icon', 'description', 'category']

class UserPrivateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPrivateData
        fields = ['full_name', 'telephone']