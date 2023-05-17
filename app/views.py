from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User
import requests
from .models import *
from .models import Favorite
from .serializers import *
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.middleware import csrf
from django.middleware.csrf import get_token
from rest_framework.permissions import IsAuthenticated
from .decorators import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta
import jwt
from django.http import FileResponse
import base64
import os
from django.utils.text import slugify
from django.http import JsonResponse
import json
# Create your views here.
# class TokenObtainPairView(BaseTokenObtainPairView):
#     serializer_class = TokenObtainPairSerializer


@permission_classes([AllowAny])
@api_view(["POST"])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Check if email is already registered
        if User.objects.filter(email=request.data["email"]).exists():
            return Response(
                {"error": "Email already registered"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save user object
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    # get user input
    username = request.data["username"]
    password = request.data["password"]
    
     # check if user exists and is active
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({"detail": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
    elif not user.is_active:
        return Response({"detail": "User is inactive"}, status=status.HTTP_400_BAD_REQUEST)

   # send payload to verify in decode
    payload = {
        "user": {
            "id": user.id,
            "email": user.email,
            "exp": (datetime.utcnow() + timedelta(minutes=15)).isoformat(),
            "iat": datetime.utcnow().isoformat(),
        }
    }
     # generate JWT tokens
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = RefreshToken.for_user(user)

    # .
    # token = {"refresh": str(refresh_token), "access": access_token}

    # create response object
    response = Response(status=status.HTTP_200_OK)
    response['Authorization'] = f'Bearer {access_token}'
    response['Refresh-Token'] = str(refresh_token)
    return response


@func_token_required
@api_view(["GET"])
def get_user(request):
    try:
        user = User.objects.all()
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@func_token_required
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@func_token_required
@api_view(["DELETE"])
# @func_token_required
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view(["POST"])
# def login_user(request):
#     # get user input
#     username = request.data["username"]
#     password = request.data["password"]

#     # check email has registered
#     user = authenticate(request, username=username, password=password)

#     token_url = "https://web-production-e388.up.railway.app/o/token/"
#     data = {
#         "grant_type": "password",
#         "username": username,
#         "password": password,
#         "client_id": settings.CLIENT_ID,
#         "client_secret": settings.CLIENT_SECRET,
#     }

#     try:
#         response = requests.post(
#             token_url,
#             data=data,
#             headers={
#                 "X-CSRFToken": csrf.get_token(request),
#                 "Content-Type": "application/x-www-form-urlencoded",
#             },
#         )
#         response.raise_for_status()
#         full_token = response.json()
#         access_token = response.json().get("access_token")
#         refresh_token = response.json().get("refresh_token")

#         headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Content-Type": "application/json",
#             "refresh_token": refresh_token,
#         }
#         res = Response()

#     except requests.exceptions.HTTPError as error:
#         return Response(
#             {"detail": "Could not get access token"},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )

#     # return token in response
#     return Response(
#         # {"oauth_token": full_token},
#         status=status.HTTP_200_OK,
#         headers=headers,
#     )

# @api_view(["POST"])
# def token(request):
#     r = requests.post(
#         "http://localhost:8000/o/token/",
#         data={
#             "grant_type": "password",
#             "username": request.data["username"],
#             "password": request.data["password"],
#             "client_id": settings.CLIENT_ID,
#             "client_secret": settings.CLIENT_SECRET,
#         },
#     )
#     return Response(r.json())


# @api_view(["POST"])
# def refresh_token(request):
#     r = requests.post(
#         "http://localhost:8000/o/token/",
#         data={
#             "grant_type": "refresh_token",
#             "refresh_token": request.data["refresh_token"],
#             "client_id": settings.CLIENT_ID,
#             "client_secret": settings.CLIENT_SECRET,
#         },
#     )
#     return Response(r.json())


@func_token_required
@api_view(['POST'])
def create_chatroom(request):
    if request.user.is_anonymous:
        return Response({"error":"User not authenticated"}, status=400)
    
    data = {'user1': request.user.id, **request.data}
    serializer = OneChatSerializer(data=data)
    
    if serializer.is_valid():
        chatroom = serializer.save(user1=request.user)
        return Response({'id': chatroom.id, 'code': chatroom.code})
    else:
        return Response(serializer.errors, status=400)


@func_token_required
@api_view(['GET'])
def view_chatroom(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    serializer = OneChatSerializer(chatroom)
    return Response(serializer.data)

@func_token_required
@api_view(['POST'])
def join_chatroom(request):
    code = request.data.get('code')
    chatroom = get_object_or_404(ChatRoom, code=code)
    if chatroom.user2 is None:
        # throw error if request.user is user1
        if chatroom.user1 == request.user:
            return Response({'detail': 'You are the owner of the chat room.'}, status=400)

        chatroom.user2 = request.user
        chatroom.save()
       
        return Response({'id': chatroom.id, 'name': chatroom.name})
    else:
        return Response({'detail': 'Chat room is already full.'}, status=400)

@func_token_required
@api_view(['DELETE'])
def delete_chatroom(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    chatroom.delete()
    return Response(status=204)

# --- message ----

@api_view(['POST'])
@func_token_required
def create_one_chat_message(request,chat_room_id):
    # chat_room_id = request.data.get("chat_room_id", None)
    try:
        chat_room = ChatRoom.objects.get(id=chat_room_id)
    except ChatRoom.DoesNotExist:
        return Response(
            {"error": f"Chat room with id={chat_room_id} does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )

    receiver_id = request.data.get("receiver", None)
    # Get the receiver from the receiver_id parameter
    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return Response(
            {"error": f"User with id={receiver_id} does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Create a new message object and populate it with data from the request
    message = OneChatMessage(
        chat_room_id=chat_room, sender=request.user, receiver=receiver
    )

    if "attachment" in request.data:
        # save the attachment to a FileField
        message.attachment.save(
            request.data["attachment"].name, request.data["attachment"], save=True
        )

    # set the text field of the message
    message.text = request.data.get("text")

    # save the message object
    message.save()

    serializer = OneChatMessageSerializer(message)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

@func_token_required
@api_view(['GET'])
def list_one_chat_messages(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    # print(request.user.id)
    # if request.user.id != chat_room.user1.id or chat_room.user2.id:
    #     return Response(
    #         {"error": "You are not a member of this chat room."},
    #         status=status.HTTP_400_BAD_REQUEST,
    #     )
    queryset = OneChatMessage.objects.filter(chat_room_id=chat_room_id)
    serializer = OneChatMessageSerializer(queryset, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@func_token_required
@api_view(['PUT'])
def update_one_chat_message(request, message_id):
    message = get_object_or_404(OneChatMessage, id=message_id)
    if request.user != message.sender:
        return Response(
            {"error": "You are not the sender of this message."},
            status=status.HTTP_403_FORBIDDEN,
        )
    serializer = OneChatMessageSerializer(
        message, data=request.data, partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@func_token_required
@api_view(['DELETE'])
def delete_one_chat_message(request, message_id):
    message = get_object_or_404(OneChatMessage, id=message_id)
    if request.user != message.sender:
        return Response(
            {"error": "You are not the sender of this message."},
            status=status.HTTP_403_FORBIDDEN,
        )
    message.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# @func_token_required
@api_view(['POST'])
def add_song(request):
    serializer = SongSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_songs(request):
    songs = Song.objects.all()
    serializer = SongSerializer(songs, many=True, context={'request': request})
    return Response(serializer.data)
    
# @func_token_required
@api_view(['PUT'])
def update_song(request, song_id):
    try:
        song = Song.objects.get(id=song_id)
    except:
        return Response({"message":"invalid id"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = SongSerializer(song, data=request.data, context={'request': request})
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @func_token_required
@api_view(['DELETE'])
def delete_song(request,song_id):
    song = get_object_or_404(Song,id=song_id)
    song.delete()
    return Response({"message":"successfully deleted"})

# @func_token_required
# @api_view(['POST'])
# def add_to_favorites(request,song_id):
    try:
        song = Song.objects.get(id=song_id)
    except Song.DoesNotExist:
        return Response({'error': 'Song not found'}, status=404)
    # add to favorite
    favorites, created = Favorite.object.get_or_create(user=request.user, song=song)

    if not created:
        #  delete it to remove the song from the user's favorites
        favorites.delete()
        message = 'Song removed from favorites'
    else:
        message = 'Song added to favorites'

    return Response({'message': message})