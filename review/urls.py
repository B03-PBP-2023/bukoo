from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('review/<int:book_id>/reviews/', views.get_reviews_by_book, name='get_reviews_by_book'),
    path('review/<int:book_id>/create_review/', views.create_review, name='create_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:book_id>/get_review_json/', views.get_review_json, name='get_review_json'),
    path('review/get_all_user_reviews/', views.get_all_user_reviews, name='get_all_user_reviews'),
]
