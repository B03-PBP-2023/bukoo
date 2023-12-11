from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('profile/', views.profile_data, name = 'user-profile'),
    path('profile/edit-profile/', views.edit_profile, name = 'edit-profile'),
    path('api/profile/bookmark-book/', views.bookmarking_books, name = 'bookmark-book'),
    path('api/delete-bookmark/', views.delete_bookmark, name = 'delete-bookmark'),
    
]