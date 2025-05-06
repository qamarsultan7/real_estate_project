from django.db import models

# Create your models here.
class ChatRooms(models.Model):
    id=models.AutoField(primary_key=True)
    user1=models.CharField(max_length=255)
    user2=models.CharField(max_length=255)
    last_message=models.TextField()
    last_message_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ChatRoom({self.user1}, {self.user2})"
    
class Messages(models.Model):
    id =models.AutoField(primary_key=True)
    chatroom=models.ForeignKey(ChatRooms, on_delete=models.CASCADE, related_name='messages')
    sender=models.CharField(max_length=255)
    message=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message({self.sender}, {self.timestamp})"