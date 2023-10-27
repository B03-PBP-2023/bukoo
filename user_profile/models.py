from django.db import models
from auth.models import User
from book_collection.models import Book

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    about_user = models.TextField()
    date_of_birth = models.CharField(max_length=10)
    gender = models.CharField(max_length=20)
    prefered_genre = models.CharField(max_length=40)

class Bookmark(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)





