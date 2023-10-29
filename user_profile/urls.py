from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('edit-profile/', views.edit_profile, name = 'edit-profile'),
    path('', views.profile_data, name = 'user-profile'),
    path('bookmark-book/', views.bookmarking_books, name = 'bookmark-book'),
    path('delete-bookmark/', views.delete_bookmark, name = 'delete-bookmark'),
    
]