from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('edit-profile', views.edit_profile, name = 'edit-profile'),
    path('user-profile', views.profile_data, name = 'user-profile'),
]