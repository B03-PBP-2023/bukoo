from django.urls import path
from auth.views import login_user, register, logout_user

urlpatterns = [
  path('auth/login/', login_user, name='login_user'),
  path('auth/register/', register, name='register'),
  path('auth/logout/', logout_user, name='logout_user'),
]