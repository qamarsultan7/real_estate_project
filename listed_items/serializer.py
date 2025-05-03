from rest_framework import serializers
from .models import ListedItem, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'is_main']

class PropertyImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_main']

class ListedItemSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ListedItem
        fields = [
            'id', 'name', 'description', 'location', 'price',
            'property_type', 'bedroom_count', 'bathroom_count',
            'kitchen_count', 'living_room_count', 'images'
        ]

class ListedItemCreateSerializer(serializers.ModelSerializer):
    images = PropertyImageCreateSerializer(many=True, required=False)
    
    class Meta:
        model = ListedItem
        fields = [
            'name', 'description', 'location', 'price',
            'property_type', 'bedroom_count', 'bathroom_count',
            'kitchen_count', 'living_room_count', 'images'
        ]
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        property_listing = ListedItem.objects.create(**validated_data)
        
        for image_data in images_data:
            PropertyImage.objects.create(property=property_listing, **image_data)
        
        return property_listing