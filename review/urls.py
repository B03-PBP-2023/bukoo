from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:book_id>/reviews/', views.get_reviews_by_book, name='get_reviews_by_book'),
    path('book/<int:book_id>/add_review/', views.create_review, name='create_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
]
