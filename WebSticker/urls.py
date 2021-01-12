"""WebSticker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from user_web_interface import views

urlpatterns = [
    path("", views.home, name='home'),
    path('new_game', views.create_new_game, name='new_game'),
    path('new_mashine_game', views.create_new_mashine_game, name='new_mashine_game'),
    path('make_a_move/<int:game_id>', views.make_a_move, name='make_a_move'),
    path('make_a_mashine_move/<int:game_id>', views.make_a_mashine_move, name='make_a_mashine_move'),
    path('game/<int:game_id>', views.view_round, name='view_round'),
    path('end_round/<int:game_id>', views.end_round, name='end_round'),
    path('end_game/<int:game_id>', views.end_game, name='end_game'),
    path('admin', views.admin_page, name='admin'),
    path('', include('pwa.urls')),
]
