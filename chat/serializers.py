from rest_framework import serializers
from .models import ChatRooms, Messages

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRooms
        fields = '__all__'
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
        
    def to_representation(self, instance):
        """
        Override to format the representation for API responses.
        """
        representation = super().to_representation(instance)
        # Convert timestamp to ISO format if it exists
        if 'timestamp' in representation and representation['timestamp']:
            # If timestamp is a datetime object, convert to ISO
            if hasattr(instance.timestamp, 'isoformat'):
                representation['timestamp'] = instance.timestamp.isoformat()
                
        return representation
