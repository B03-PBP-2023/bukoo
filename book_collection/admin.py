from django.contrib import admin
from book_collection.models import Book, Genre, MockAuthorProfile
# Register your models here.
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(MockAuthorProfile)