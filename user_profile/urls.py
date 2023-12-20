from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('profile/', views.profile_data, name = 'user-profile'),
    path('profile/edit-profile/', views.edit_profile, name = 'edit-profile'),
    path('api/profile/bookmark-book/<int:book_id>/', views.bookmarking_books, name = 'bookmark-book'),
    path('api/profile/delete-bookmark/<int:book_id>/', views.delete_bookmark, name = 'delete-bookmark'),
    path('api/profile/get-bookmark-status/<int:book_id>/', views.get_bookmark_status, name = 'get-bookmark-status'),
    path('profile/json/', views.show_json, name = 'show_profile-json'),
    path('profile/xml/', views.show_xml, name = 'show_profile_xml'),
    path('profile/xml/<int:id>/', views.show_xml_id, name = 'profile_xml_id'),
    path('profile/json/<int:id>/', views.show_json_id, name = 'profile_json_id'),
]