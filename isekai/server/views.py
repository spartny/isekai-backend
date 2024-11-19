from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
import json
from django.db.models import F
import requests
from .models import Game, User
from .gamebuilder import start_game, continue_game

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

    print("Received username:", username)  
    print("Received password:", password)  

    try:
        user = User.objects.get(username=username) 
        if (user.password == password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
    except User.DoesNotExist:
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

def get_saved_games(request):
    username = request.GET.get("username")
    user = User.objects.get(username=username)
    games = Game.objects.filter(user_id=user.id).values("id", "game_title", "genre", "chat_log", "current_context", "saved_at")

    print(len(list(games)))
    return JsonResponse({"games": list(games)}, status=200)

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def start_new_game(request):
    data = json.loads(request.body)
    username = data.get("username")
    genre_choice = data.get("genre")
    game_title = data.get("title")
    print(username, genre_choice, game_title)

    # Get the generated game data
    game_data = start_game(genre_choice)
    print(game_data)

    # Create a new game in the database
    game = Game.objects.create(
        user=User.objects.get(username=username),
        genre=game_data["genre"],
        game_title=game_title,
        chat_log=[{"user_input": None, "generated_response": game_data["story"]}],
        current_context=game_data["story"],
    )
    return JsonResponse({
        "message": "New game started.",
        "game_id": game.id,
        "story": game_data["story"],
    }, status=201)


@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def continue_old_game(request):
    data = json.loads(request.body)
    username = data.get("username")
    genre_choice = data.get("genre")
    story = data.get("story")
    user_input = data.get('message')
    game_title= data.get("title")
    print(username, story, genre_choice, user_input)

    # Get the generated game data
    game_data = continue_game(user_input, genre_choice, story)
    print(game_data)

    # Create a new game in the database
    game = Game.objects.filter(
        user_id=User.objects.get(username=username).id,
        game_title=game_title
    ).first()

    if game:
        game.chat_log.append({
            "user_input": user_input,
            "generated_response": game_data["story"]
        })
        game.current_context += game_data["story"]
        game.save()

        return JsonResponse({
                "message": "Game continued.",
                "game_id": game.id,
                "story": game_data["story"],
            }, status=201)
    else:
        return JsonResponse({"error": "Game not found."}, status=404)
    
@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_game(request):
    data = json.loads(request.body)
    game_id = data.get("id")
    Game.objects.filter(id=game_id).delete()
    return JsonResponse({"message": "Game deleted."}, status=200)

# @csrf_exempt
# def update_profile(request):
#     data = json.loads(request.body)
#     user_id = data.get("user_id")
#     username = data.get("username")
#     email = data.get("email")

#     user = get_object_or_404(User, id=user_id)
#     user.username = username
#     user.email = email
#     user.save()
#     return JsonResponse({"message": "Profile updated successfully."}, status=200)

# @csrf_exempt
# def logout_user(request):
#     data = json.loads(request.body)
#     user_id = data.get("user_id")
    
#     user = get_object_or_404(User, id=user_id)
#     user.session_token = None
#     user.save()
#     return JsonResponse({"message": "Logged out successfully."}, status=200)

