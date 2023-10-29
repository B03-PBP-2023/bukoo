from django.urls import path
from admin_dashboard import views

urlpatterns = [
    path('admin/api/book_list/', views.get_book_list, name='get_book_list'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
]

