from django.db import models
from django.contrib.auth import get_user_model
import json
from .models import ChatRooms, Messages
from .serializers import ChatRoomSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['POST'])
def send_message(request):
    try:
        data = request.data
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        message_text = data.get('message')
        chatroom_id = data.get('chatroom_id', None)
        
        # Validate required fields
        if not sender_id or not message_text:
            return Response(
                {"status": False, "message": "sender_id and message are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # If chatroom_id is provided, use existing room
        if chatroom_id:
            try:
                chatroom = ChatRooms.objects.get(id=chatroom_id)
            except ChatRooms.DoesNotExist:
                return Response(
                    {"status": False, "message": "Chat room not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        # If no chatroom_id but receiver_id, find or create a room
        elif receiver_id:
            # Check if a chat room already exists between these users
            chatroom = ChatRooms.objects.filter(
                models.Q(user1=sender_id, user2=receiver_id) | 
                models.Q(user1=receiver_id, user2=sender_id)
            ).first()
            
            # If no chat room exists, create one
            if not chatroom:
                chatroom_data = {
                    'user1': sender_id,
                    'user2': receiver_id,
                    'last_message': message_text
                }
                chatroom_serializer = ChatRoomSerializer(data=chatroom_data)
                if chatroom_serializer.is_valid():
                    chatroom = chatroom_serializer.save()
                else:
                    return Response(
                        {"status": False, "message": "Validation error", "errors": chatroom_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response(
                {"status": False, "message": "Either chatroom_id or receiver_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create the message
        message_data = {
            'chatroom': chatroom.id,
            'sender': sender_id,
            'message': message_text
        }
        message_serializer = MessageSerializer(data=message_data)
        if message_serializer.is_valid():
            message = message_serializer.save()
            
            # Update the chat room's last message
            chatroom.last_message = message_text
            chatroom.save()
            
            return Response({
                "status": True,
                "message": "Message sent successfully",
                "data": {
                    'message_id': message.id,
                    'chatroom_id': chatroom.id,
                    'timestamp': message.timestamp.isoformat()
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"status": False, "message": "Validation error", "errors": message_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        return Response(
            {"status": False, "message": f"An error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_chat_rooms(request):
    try:
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response(
                {"status": False, "message": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Get all chat rooms for this user
        chat_rooms = ChatRooms.objects.filter(
            models.Q(user1=user_id) | models.Q(user2=user_id)
        ).order_by('-updated_at')
        
        User = get_user_model()
        result = []
        
        for room in chat_rooms:
            # Determine which user is the other person in the chat
            other_user_id = room.user2 if str(room.user1) == str(user_id) else room.user1
            
            try:
                other_user = User.objects.get(id=other_user_id)
                
                # Get profile picture URL - adjust field name as per your User model
                profile_pic = None
                if hasattr(other_user, 'profile_image'):
                    profile_pic = other_user.profile_pic.url if other_user.profile_pic else None
                elif hasattr(other_user, 'avatar'):
                    profile_pic = other_user.avatar.url if other_user.avatar else None
                elif hasattr(other_user, 'image'):
                    profile_pic = other_user.image.url if other_user.image else None
                
                room_data = {
                    'chatroom_id': room.id,
                    'other_user_id': other_user_id,
                    'other_user_name': other_user.username,
                    'other_user_profile_pic': profile_pic,
                    'last_message': room.last_message,
                    'unread_count': Messages.objects.filter(
                        chatroom=room, 
                        sender=other_user_id, 
                        is_read=False
                    ).count() if hasattr(Messages, 'is_read') else 0
                }
                result.append(room_data)
                
            except User.DoesNotExist:
                # Skip this room if the other user doesn't exist
                continue
        
        return Response(
            {"status": True, "message": "Chat rooms retrieved successfully", "chat_rooms": result},
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {"status": False, "message": f"An error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_messages(request):
    try:
        room_id = request.query_params.get('room_id')
        
        if not room_id:
            return Response(
                {"status": False, "message": "room_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Verify the room exists
        try:
            chatroom = ChatRooms.objects.get(id=room_id)
        except ChatRooms.DoesNotExist:
            return Response(
                {"status": False, "message": "Chat room not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get all messages for this room
        messages = Messages.objects.filter(chatroom=chatroom).order_by('timestamp')
        
        # Mark all unread messages as read if there's an is_read field
        if hasattr(Messages, 'is_read'):
            # Assuming we have a user_id parameter to know which messages to mark as read
            user_id = request.query_params.get('user_id')
            if user_id:
                # Use field lookup with 'exact' instead of 'ne'
                unread_messages = messages.exclude(sender=user_id).filter(is_read=False)
                unread_messages.update(is_read=True)
        
        # Serialize the messages
        serializer = MessageSerializer(messages, many=True)
        
        return Response({
            "status": True, "message": "Messages retrieved successfully",
            "chatroom_id": room_id,
            "messages": serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"status": False, "message": f"An error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )