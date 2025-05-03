from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ListedItem
from .serializer import (
    ListedItemSerializer, 
    ListedItemCreateSerializer,
    PropertyImageSerializer
)

class ListedItemListView(generics.ListAPIView):
    queryset = ListedItem.objects.all()
    serializer_class = ListedItemSerializer

class ListedItemCreateView(generics.CreateAPIView):
    serializer_class = ListedItemCreateSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        property_data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'location': request.data.get('location'),
            'price': request.data.get('price'),
            'property_type': request.data.get('property_type'),
            'bedroom_count': request.data.get('bedroom_count'),
            'bathroom_count': request.data.get('bathroom_count'),
            'kitchen_count': request.data.get('kitchen_count'),
            'living_room_count': request.data.get('living_room_count')
        }
        
        serializer = self.get_serializer(data=property_data)
        serializer.is_valid(raise_exception=True)
        property_instance = serializer.save()
        
        # Handle image uploads
        images = request.FILES.getlist('images')
        
        for i, image in enumerate(images):
            is_main_value = False
            if is_main and i < len(is_main):
                is_main_value = is_main[i] in ['true', 'True', '1']
                
            PropertyImage.objects.create(
                property=property_instance,
                image=image,
                is_main=is_main_value
            )
        
        return Response(
            ListedItemSerializer(property_instance).data,
            status=status.HTTP_201_CREATED
        )