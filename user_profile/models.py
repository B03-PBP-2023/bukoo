from django.db import models
from auth.models import User
from book_collection.models import Book

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    about_user = models.TextField(null=True)
    date_of_birth = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=20, null=True)
    prefered_genre = models.CharField(max_length=40, null=True)

    def natural_key(self):
        return {'id':self.pk, 'name':self.user.username}

class Bookmark(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)