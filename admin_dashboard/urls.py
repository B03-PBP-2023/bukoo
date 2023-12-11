from django.urls import path
from admin_dashboard import views
app_name = 'admin_dashboard'

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin-dashboard/create_book/', views.create_book, name='create_book'),
    path('admin-dashboard/admin2/', views.admin2, name='admin2'),
    
    path('api/admin-dashboard/book_list/', views.get_book_list, name='get_book_list'),
    path('api/admin-dashboard/book_status/', views.book_status, name='book_status'),
    path('api/admin-dashboard/xml/', views.show_xml, name='show_xml'),
    path('api/admin-dashboard/json/', views.show_json, name='show_json'), 
    path('api/admin-dashboard/xml/<int:id>/', views.show_xml_id, name='show_xml_id'),
    path('api/admin-dashboard/json/<int:id>/', views.show_json_id, name='show_json_id'),
]
