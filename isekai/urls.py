"""
URL configuration for isekai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .server.views import test_view, login_view, protected_view, signup_user, oauth_view, oauth_success_view, get_saved_games, start_new_game, continue_old_game #, update_profile, logout_user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
import oauth2_provider.views as oauth2_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test_view, name='test_view'),
    path('login/', login_view, name='login'),  # Get tokens
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh tokens
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # path("", include("allauth.urls")), #most important
    path("oauth/google/", oauth_view, name="google_oauth_view"),
    path("google/login/callback/", oauth_success_view, name="google_oauth_view"),
    # path('auth/', include('dj_rest_auth.urls')),
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('auth/social/', include('allauth.socialaccount.urls')),  # This is for social authentication
    path('get-saved-games/', get_saved_games, name='get_saved_games'),
    path('start-new-game/', start_new_game, name='start_new_game'),
    path('signup_user/', signup_user, name='signup_user'),
    path('continue-old-game/', continue_old_game, name='continue_old_game')
]


