from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Assuming passwords are hashed
    session_token = models.CharField(max_length=255, blank=True, null=True)  # Optional, for session management
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class Game(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    game_title = models.CharField(max_length=255, default="Untitled Game")
    genre = models.CharField(max_length=50)
    chat_log = models.JSONField(default=list)  # Stores structured chat data
    current_context = models.TextField(default='')
    saved_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.game_title} ({self.genre}) - {self.user.username}"

