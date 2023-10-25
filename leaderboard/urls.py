from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:book_id>/popular/', views.get_popular_books, name='get_popular_books'),
    path('book/<int:book_id>/best/', views.get_best_books, name='get_best_books'),
    path('book/<int:book_id>/ratings/', views.get_ratings_by_user, name='get_ratings_by_user'),
    path('book/<int:book_id>/create_rating/', views.create_rating, name='create_rating'),
    path('leaderboard/<int:review_id>/delete/', views.delete_rating, name='delete_rating'),
    path('leaderboard/<int:review_id>/edit/', views.edit_rating, name='edit_rating'),
    path('leaderboard/<int:review_id>/recommendation_count/', views.get_user_recommendation_count, name='get_user_recommendation_count'),
]