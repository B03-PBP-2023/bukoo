from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:book_id>/popular/', views.get_popular_books, name='get_popular_books'),
    path('book/ratings/', views.get_ratings_by_user, name='get_ratings_by_user'),
    path('book/<int:book_id>/create_rating/', views.create_rating, name='create_rating'),
    path('leaderboard/<int:book_id>/delete/', views.delete_rating, name='delete_rating'),
    path('', views.leaderboard_view, name='leaderboard_view'),
]
