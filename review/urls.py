from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('<int:book_id>/reviews/', views.get_reviews_by_book, name='get_reviews_by_book'),
    path('<int:book_id>/create_review/', views.create_review, name='create_review'),
    path('<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('<int:book_id>/get_review_json/', views.get_review_json, name='get_review_json'),
]
