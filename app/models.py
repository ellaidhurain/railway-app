from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
# Create your models here.
import random

def generate_random_code():
    code = ''.join(str(random.randint(0, 9)) for i in range(6))
    return code


class ChatRoom(models.Model):
    name = models.CharField(max_length=50, unique=True) 
    user1 = models.ForeignKey(User, related_name='chat_rooms_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chat_rooms_as_user2', default=None, null=True, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=10, unique=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_random_code()
        super().save(*args, **kwargs)


class OneChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    chat_room_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', default=None, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='files',validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg'])], null=True)
    
   