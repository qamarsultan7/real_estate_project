from .views import send_message, get_chat_rooms,get_messages
from django.urls import path

urlpatterns = [
    path('send-message/', send_message, name='send_message'),
    path('get-messages/<uuid:room_id>', get_messages, name='get_messages'),
    path('get-room/<uuid:user_id>',get_chat_rooms,name='get_chat_rooms'),
]