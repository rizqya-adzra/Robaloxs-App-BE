from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.users.models import User, UserProfile, UserPrivateData, Badge

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Email atau password salah.")

class UserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['name', 'level', 'icon', 'description', 'category']
        read_only_fields = fields

class UserPrivateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPrivateData
        fields = ['full_name', 'telephone']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'avatar_url', 'total_spendings', 'weekly_spendings']
        read_only_fields = ['total_spendings', 'weekly_spendings']

class MeSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    private_data = UserPrivateDataSerializer()
    badge = UserBadgeSerializer(read_only=True) 

    class Meta:
        model = User
        fields = ['email', 'is_staff', 'profile', 'private_data', 'badge']
        read_only_fields = ['email', 'is_staff', 'badge']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        private_data_data = validated_data.pop('private_data', {})
        instance = super().update(instance, validated_data)
        if profile_data:
            profile_obj = instance.profile
            for attr, value in profile_data.items():
                setattr(profile_obj, attr, value)
            profile_obj.save()

        if private_data_data:
            private_obj = instance.private_data
            for attr, value in private_data_data.items():
                setattr(private_obj, attr, value)
            private_obj.save()
        return instance