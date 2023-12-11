from django.urls import path
from . import views

app_name = 'leaderboard'

urlpatterns = [
    path('api/leaderboard/popular/', views.get_popular_books, name='get_popular_books'),
    path('api/leaderboard/ratings/', views.get_ratings_by_user, name='get_ratings_by_user'),
    path('api/leaderboard/book/<int:book_id>/create_rating/', views.create_rating, name='create_rating'),
    path('api/leaderboard/<int:book_id>/delete/', views.delete_rating, name='delete_rating'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard_view'),
]
