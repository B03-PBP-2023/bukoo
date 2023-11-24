from django.urls import path
from admin_dashboard import views
app_name = 'admin_dashboard'

urlpatterns = [
    path('admin/api/book_list/', views.get_book_list, name='get_book_list'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('book_status/', views.book_status, name='book_status'),
    path('create_book/', views.create_book, name='create_book'),
    path('admin2/', views.admin2, name='admin2'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'), 
    path('admin-dashboard/admin2/', views.admin2, name='admin2'),
    path('xml/<int:id>/', views.show_xml_id, name='show_xml_id'),
    path('json/<int:id>/', views.show_json_id, name='show_json_id'),

]
