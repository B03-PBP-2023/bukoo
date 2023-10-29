from django.urls import path
from book_collection import views

urlpatterns = [
  path('api/book', views.get_book_list, name='get_book_list'),
  path('api/book/<int:id>/', views.get_book_detail, name='get_book_detail'),
  path('api/book/create/', views.add_book, name='add_book'),
  path('api/book/edit/<int:id>/', views.edit_book, name='edit_book'),
  path('api/book/delete/<int:id>/', views.delete_book, name='delete_book'),
]