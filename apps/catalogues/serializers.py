from rest_framework import serializers
from .models import RobuxCategory, RobloxItem, RobloxProduct, RobloxRobux, RobloxServer

class RobuxCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RobuxCategory
        read_only_fields = '__all__'

class RobloxItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobloxItem
        read_only_fields = '__all__'

class RobloxProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobloxProduct
        read_only_fields = '__all__'

class RobloxRobuxSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobloxRobux
        read_only_fields = '__all__'

class RobloxServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobloxServer
        read_only_fields = '__all__'