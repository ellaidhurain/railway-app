import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import random
from django.forms import ValidationError

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
    
   
class Song(models.Model):
    title = models.TextField(max_length=100, null=True)
    audio_file = models.FileField(upload_to='audio/', default=None)
    genre = models.CharField(max_length=100, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='files',validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])], default=None)
    artist_name = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.title

    def clean(self):
        """
        Check that the file size is less than 10MB.
        """
        if self.file.size > 10485760:
            raise ValidationError("The file size is too large. Maximum size is 10MB.")
        
    def validate_file(self, value):
        """
        Check that the file is an MP3 audio file.
        """
        if not value.name.endswith('.mp3'):
            raise ValidationError("Only MP3 files are allowed.")
        if not value.content_type.startswith('audio/mp3'):
            raise ValidationError("Only MP3 audio files are allowed.")
        return value
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
