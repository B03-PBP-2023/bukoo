from django.urls import path
from book_collection import views

urlpatterns = [
  path('api/book/', views.get_book_list, name='get_book_list'),
  path('api/book/<int:id>/', views.get_book_detail, name='get_book_detail'),
  path('api/book/create/', views.add_book, name='add_book'),
  path('api/book/edit/<int:id>/', views.edit_book, name='edit_book'),
  path('api/book/delete/<int:id>/', views.delete_book, name='delete_book'),
  path('api/genre/', views.get_genres, name='get_genres'),
  path('book-submission/', views.show_book_submission, name='show_book_submission'),
  path('book/<str:slug>/', views.show_book_detail, name='show_book_detail'),
  path('search/', views.show_search, name='show_search'),
  path('', views.show_landing_page, name='show_landing_page'),
]