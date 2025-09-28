from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='game/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='game/logout.html'), name='logout'),
    path('start/', views.start_game, name='start-game'),
    path('play/<int:session_id>/', views.game_play, name='game-play'),
]