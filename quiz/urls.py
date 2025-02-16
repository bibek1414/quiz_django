from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.quiz_list, name="quiz_list"),
    path("<int:quiz_id>/take/", views.take_quiz, name="take_quiz"),
    path("<int:quiz_id>/result/", views.quiz_result, name="quiz_result"),
    path('history/', views.quiz_history, name='quiz_history'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
