from django.urls import path,include,re_path
from rest_framework import routers
from .views import *

urlpatterns = [
    
    path('user', create_user, name='create_user'),
    path('user_list', get_user, name='get_user'),
    path('user/update/<int:user_id>', update_user, name='update_user'),
    path('user/delete/<int:user_id>', delete_user, name='delete_user'),
    path('login', login_user, name='login'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('chat_room/create/', create_chatroom),
    path('chat_room/<int:chatroom_id>', view_chatroom),
    path('chat_room/join', join_chatroom),
    path('chat_room/delete/<int:chatroom_id>', delete_chatroom),
    
    path('one_chat_message/send/<int:chat_room_id>', create_one_chat_message, name='one_chat_room_list'),
    path('one_chat_message/get/<int:chat_room_id>', list_one_chat_messages),
    path('one_chat_message/update/<int:message_id>', update_one_chat_message),
    path('one_chat_message/delete/<int:message_id>', delete_one_chat_message),
    
    path('lofi/add_song', add_song, name='add_song'),
    path('lofi/get_songs', get_songs, name='get_songs'),
    path('lofi/update_song/<int:song_id>', update_song, name='update_song'),
    path('lofi/delete_song/<int:song_id>', delete_song, name='delete_song'),
    # path('lofi/add_to_favorites/<int:song_id>', add_to_favorites, name='add_to_favorites'),
 
   
]
