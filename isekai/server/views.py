from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
import requests
from .models import Game

@api_view(['GET'])
def test_view(request):
    data = {"message": "This is a GET request"}
    print('noway')
    return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    print("In login")
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        # Generate token for the authenticated user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=401)


@api_view(['POST'])
@permission_classes([AllowAny])
def oauth_view(request):
    print("In oauth")
    return redirect("https://accounts.google.com/o/oauth2/v2/auth?client_id=874159592214-3bllh63hs5824e9ik23ecirdumpieqj5.apps.googleusercontent.com&redirect_uri=http://localhost:8000/google/login/callback/&response_type=code&scope=profile email&access_type=offline")

@csrf_exempt
@api_view(['GET', "POST"])
@permission_classes([AllowAny])
def oauth_success_view(request):
    print("No Way")
    try:
        # Log the request body
        data = json.loads(request.body)
        print("Received data:", data)  # Log the parsed JSON data

        # Check if the authorization code is being sent
        code = data.get('code')
        print("Authorization code:", code)

        if not code:
            return JsonResponse({"error": "Authorization code not provided"}, status=400)

        # Token exchange process
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': 'http://localhost:5173/oauth/callback/',  # Must match the original request
            'grant_type': 'authorization_code',
        }
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()

        print("Token response:", token_json)  # Log the response from Google

        if 'error' in token_json:
            return JsonResponse({"error": token_json.get('error_description')}, status=400)

        # Return the tokens
        return JsonResponse({
            'access_token': token_json.get('access_token'),
            'refresh_token': token_json.get('refresh_token'),
            'id_token': token_json.get('id_token'),  # Optional
            'expires_in': token_json.get('expires_in'),
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Restricts access to authenticated users
def protected_view(request):
    return Response({"message": "You are authenticated!"})

def get_saved_games(request, user_id):
    games = Game.objects.filter(user_id=user_id)
    game_list = [{
        "id": game.id,
        "game_title": game.game_title,
        "genre": game.genre,
        "saved_at": game.saved_at
    } for game in games]
    return JsonResponse({"games": game_list})

