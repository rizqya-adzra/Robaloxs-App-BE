from rest_framework import serializers
from apps.catalogues.models import RobuxCategory, RobloxItem, RobloxProduct, RobloxRobux
from apps.roblox_cores.models import RobloxServer

class RobuxCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RobuxCategory
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class RobuxCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RobuxCategory
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class RobloxRobuxSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=RobuxCategory.objects.all())

    class Meta:
        model = RobloxRobux
        fields = ['id', 'product_type', 'name', 'robux_amount', 'price', 'category', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = {
            "id": instance.category.id,
            "name": instance.category.name
        }
        return response

class RobloxServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobloxServer
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class RobloxItemSerializer(serializers.ModelSerializer):
    server = serializers.PrimaryKeyRelatedField(queryset=RobloxServer.objects.all())
    class Meta:
        model = RobloxItem
        fields = ['id', 'product_type', 'roblox_item_id_external', 'name', 'price', 'server', 'description', 'image_url', 'created_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['server'] = {
            "id": instance.server.id,
            "name": instance.server.name
        }
        return response

class RobloxProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobloxProduct
        fields = ['id', 'name', 'price', 'product_type', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.product_type == RobloxProduct.ProductType.ROBUX:
            try:
                robux_instance = instance.robloxrobux 
                custom_data = RobloxRobuxSerializer(robux_instance).data
                response.update(custom_data) 
            except RobloxRobux.DoesNotExist:
                response['error'] = "Data Robux detail hilang"

        elif instance.product_type == RobloxProduct.ProductType.ITEM:
            try:
                item_instance = instance.robloxitem
                custom_data = RobloxItemSerializer(item_instance).data
                response.update(custom_data)
            except RobloxItem.DoesNotExist:
                response['error'] = "Data Item detail hilang"
        return response