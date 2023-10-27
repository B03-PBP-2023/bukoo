from django.urls import path
from admin_dashboard.views import show_verif

app_name = 'admin_dashboard'

urlpatterns = [
    path('', show_verif, name='show_verif'),
]