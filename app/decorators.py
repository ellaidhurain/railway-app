from functools import wraps
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from oauth2_provider.models import AccessToken
from datetime import datetime
import jwt
from django.conf import settings
from django.contrib.auth.models import User

def func_token_required(view_func):
    def decorator(request, *args, **kwargs):
        # Get the JWT token from the Authorization header
        auth_header = request.headers.get("Authorization", "").split()
        if not auth_header or auth_header[0].lower() != "bearer":
            return JsonResponse(
                {"error": "Invalid token header. No credentials provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = auth_header[1]
        if not token:
            return JsonResponse({"error": "Token not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Decode the JWT token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload["user"]["id"]
            request.user = User.objects.get(id=user_id)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return JsonResponse({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        return view_func(request, *args, **kwargs)

    return decorator

# def func_token_required(view_func):
#     @wraps(view_func)
#     def wrapper(request, *args, **kwargs):
#         auth_header = request.headers.get("Authorization", "").split()
#         if not auth_header or auth_header[0].lower() != "bearer":
#             return JsonResponse(
#                 {"error": "Invalid token header. No credentials provided."},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         # # get the token string
#         token= auth_header[1]
#         if not token:
#             # Token cookie not found, handle error
#             return JsonResponse({"error":"token not found"}, status=status.HTTP_404_NOT_FOUND)
           
#         try:
#             access_token = AccessToken.objects.get(token=token)
#         except AccessToken.DoesNotExist:
#             return JsonResponse(
#                 {"error": "Invalid access token. Token not found."},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         # Check if the token has expired
#         expires_at = access_token.expires
#         now = datetime.utcnow().replace(tzinfo=expires_at.tzinfo)
#         if expires_at < now:
#             return JsonResponse(
#                 {"error": "The access token has expired."},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
        
#         return view_func(request, *args, **kwargs)
#     return wrapper


# def token_required(func):
#     @wraps(func)
#     def wrapper(self,request, *args, **kwargs):
#         # when using class method we need to pass self argument as first
#         # get the token from the Authorization header
#         auth_header = request.headers.get("Authorization", "").split()
#         if not auth_header or auth_header[0].lower() != "bearer":
#             return JsonResponse(
#                 {"error": "Invalid token header. No credentials provided."},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         #  get the token string
#         token= auth_header[1]
#         if not token:
#             # Token cookie not found, handle error
#             return JsonResponse({"error":"token not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         try:
#             access_token = AccessToken.objects.get(token=token)
#         except AccessToken.DoesNotExist:
#             return JsonResponse(
#                 {"error": "Invalid access token. Token not found."},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         # Check if the token has expired
#         expires_at = access_token.expires
#         now = datetime.utcnow().replace(tzinfo=expires_at.tzinfo)
#         if expires_at < now:
#             return JsonResponse(
#                 {"error": "The access token has expired."},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
        
#         # Pass token value to view function
#         return func(self,request,*args, **kwargs)
#     return wrapper
