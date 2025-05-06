from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.contrib.auth import get_user_model
import json
from .models import ChatRooms, Messages
from rest_framework.decorators import api_view

@api_view(['POST'])
def send_message(request):
    try:
        data = json.loads(request.body)
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        message_text = data.get('message')
        chatroom_id = data.get('chatroom_id', None)
        # Validate required fields
        if not sender_id or not message_text:
            return JsonResponse({'error': 'sender_id and message are required'}, status=400)
            
        # If chatroom_id is provided, use existing room
        if chatroom_id:
            try:
                chatroom = ChatRooms.objects.get(id=chatroom_id)
            except ChatRooms.DoesNotExist:
                return JsonResponse({'error': 'Chat room not found'}, status=404)
        # If no chatroom_id but receiver_id, find or create a room
        elif receiver_id:
            # Check if a chat room already exists between these users
            chatroom = ChatRooms.objects.filter(
                models.Q(user1=sender_id, user2=receiver_id) | 
                models.Q(user1=receiver_id, user2=sender_id)
            ).first()
            
            # If no chat room exists, create one
            if not chatroom:
                chatroom = ChatRooms.objects.create(
                    user1=sender_id,
                    user2=receiver_id,
                    last_message=message_text
                )
        else:
            return JsonResponse({'error': 'Either chatroom_id or receiver_id is required'}, status=400)
        
        # Create the message
        message = Messages.objects.create(
            chatroom=chatroom,
            sender=sender_id,
            message=message_text
        )
        
        # Update the chat room's last message
        chatroom.last_message = message_text
        chatroom.save()
        
        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'chatroom_id': chatroom.id,
            'timestamp': message.timestamp.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def get_chat_rooms(request):
    try:
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'user_id is required'}, status=400)
            
        # Get all chat rooms for this user
        chat_rooms = ChatRooms.objects.filter(
            models.Q(user1=user_id) | models.Q(user2=user_id)
        ).order_by('-updated_at')  # Assuming you have an updated_at field
        
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
                    'other_user_name': other_user.username,  # Adjust as needed
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
        
        return JsonResponse({'chat_rooms': result})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@api_view(['GET'])
def get_messages(request):
    try:
        room_id = request.GET.get('room_id')
        
        if not room_id:
            return JsonResponse({'error': 'room_id is required'}, status=400)
            
        # Verify the room exists
        try:
            chatroom = ChatRooms.objects.get(id=room_id)
        except ChatRooms.DoesNotExist:
            return JsonResponse({'error': 'Chat room not found'}, status=404)
        
        # Get all messages for this room
        messages = Messages.objects.filter(chatroom=chatroom).order_by('timestamp')
        
        # Mark all unread messages as read if there's an is_read field
        if hasattr(Messages, 'is_read'):
            # Assuming we have a user_id parameter to know which messages to mark as read
            user_id = request.GET.get('user_id')
            if user_id:
                unread_messages = messages.filter(sender__ne=user_id, is_read=False)
                unread_messages.update(is_read=True)
        
        # Format the messages
        result = []
        for message in messages:
            msg_data = {
                'id': message.id,
                'sender_id': message.sender,
                'message': message.message,
                'timestamp': message.timestamp.isoformat()
            }
            if hasattr(message, 'is_read'):
                msg_data['is_read'] = message.is_read
            
            result.append(msg_data)
        
        return JsonResponse({
            'chatroom_id': room_id,
            'messages': result
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)