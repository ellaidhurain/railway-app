from rest_framework import serializers
from .models import ChatRoom, OneChatMessage, Song, Favorite
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class OneChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'
        # depth = 1
        
    def create(self, validated_data):
        return ChatRoom.objects.create(**validated_data)
        
class OneChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneChatMessage
        fields = '__all__'
        # depth = 1


class SongSerializer(serializers.ModelSerializer):
    audio_file_url = serializers.SerializerMethodField()
    attachment_url = serializers.SerializerMethodField()
    class Meta:
        model = Song
        fields =   fields = ('id', 'audio_file_url', 'attachment_url', 'title', 'genre', 'creation_date','audio_file','attachment')
    
    def get_audio_file_url(self, obj):
        if obj.audio_file:
            return self.context['request'].build_absolute_uri(obj.audio_file.url)
        return None
    
    def get_attachment_url(self, obj):
        if obj.attachment:
            return self.context['request'].build_absolute_uri(obj.attachment.url)
        return None
    
        

class Favorite(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'