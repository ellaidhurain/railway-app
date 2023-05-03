from rest_framework import serializers
from .models import *
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
